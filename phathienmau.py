import  cv2
import numpy as np

tong_area = 0
area_1 = 0
box_0 = []
box_1 = []
def detect_color_object (frame):
    tong_area = 0
    # area_1 = 0
    # box_0 = []
    # box_1 = []
    kernel = np.ones((3, 3), np.uint8)  # Kernel 3x3 với các giá trị 1
    kernel_1 = np.ones((9, 9), np.uint8)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  
    # Ngưỡng màu để detect thung
    lower_1 = np.array([10,50,150])  #giới hạn màu thùng giấy
    upper_1 = np.array([20,150,255])
    gray_1 = cv2.inRange(hsv,lower_1,upper_1)

    # Hàm dilate và erode để làm mịn và loại bỏ nhiễu
    gray_1 = cv2.dilate(gray_1, kernel_1, iterations=1)         
    gray_1 = cv2.dilate(gray_1, kernel, iterations=1)
    gray_1 = cv2.erode(gray_1, kernel_1, iterations=1)          # Hàm erode để loại bỏ nhiễu
    gray_1 = cv2.erode(gray_1, kernel, iterations=1)
    #gray_1 = cv2.dilate(gray_1, kernel_1, iterations=1)
    cv2.imshow("gray_1",gray_1) 
    
    # Tìm các đường viền của thùng 
    contours_1, hierarchy_1 = cv2.findContours(gray_1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for i, ct in enumerate(contours_1):
        if hierarchy_1[0][i][3] == -1:
                area = cv2.contourArea(ct)
                if area > 500:
                    tong_area = tong_area + area
                    rect = cv2.minAreaRect(ct)
                    box = cv2.boxPoints(rect)
                    box = box.astype(int)
                    cv2.drawContours(frame, [box], 0, (255, 255, 0), 4)
    return frame

def detect_iron_contours(frame):
    global kernel,kernel_1,hsv
    #detect viền của thanh sắt 
    lower = np.array([0,120,120])  # giới hạn màu thanh sắt
    upper = np.array([15,255,255])
    gray = cv2.blur(hsv, (3, 3))  # Kích thước kernel là 5x5 , làm mịn khung hình bằng blur 
    gray = cv2.inRange(gray,lower,upper)

    gray = cv2.erode(gray, kernel, iterations=1)
    gray = cv2.dilate(gray, kernel, iterations=1)
    gray = cv2.erode(gray, kernel_1, iterations=1)
    gray = cv2.erode(gray, kernel_1, iterations=1)
    #gray = cv2.erode(gray, kernel, iterations=1)
    gray = cv2.dilate(gray, kernel_1, iterations=1)
    gray = cv2.dilate(gray, kernel_1, iterations=1)

    # cv2.imshow("gray",gray)
    # Tìm đường viền cho thanh sắt 
    contours, hierarchy = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # Hàm để lấy giá trị y nhỏ nhất của một contour
    def get_min_y(contour):
        return contour[contour[:, :, 1].argmin()][0][1]

    # Sắp xếp các contours theo giá trị y nhỏ nhất
    sorted_contours = sorted(contours, key=get_min_y)

    if len(contours) > 1:
        for i,ct in enumerate(sorted_contours):
            area = cv2.contourArea(ct)
            if area > 500:
                # Giả sử 'ct' là contour đã được xác định
                rect = cv2.minAreaRect(ct)
                box = cv2.boxPoints(rect)
                box = box.astype(int)
                #cv2.drawContours(frame, [box], 0, (255, 0, 255), 2)

                # Sắp xếp các điểm góc của hình chữ nhật theo thứ tự từ trên xuống dưới
                sorted_points = sorted(box, key=lambda x: x[1])

                if abs(sorted_points[0][0]-sorted_points[1][0]) < abs(sorted_points[0][0]-sorted_points[2][0]):
                    sorted_points[1],sorted_points[2]=sorted_points[2],sorted_points[1]
                if i == 0:
                    box_0 = sorted_points # cạnh dươi là điểm thứ 2 và 3
                elif i == 1:
                    box_1 = sorted_points # cạnh trên là điểm thứ 0 và 1
        if len(box_0)>0 and len(box_1)>0:
            pts = np.array([box_0[3],box_0[2],box_1[0],box_1[1]], np.int32)
            pts = cv2.convexHull(pts)
            pts = pts.reshape((-1, 1, 2))
            x1, y1 = pts[0][0][0], pts[0][0][1]
            x2, y2 = pts[1][0][0], pts[1][0][1]
            x3, y3 = pts[2][0][0], pts[2][0][1]
            x4, y4 = pts[3][0][0], pts[3][0][1]

            area_1 = 0.5 * abs(
                (x1 * y2) + (x2 * y3) + (x3 * y4) + (x4 * y1) - (y1 * x2) - (y2 * x3) - (y3 * x4) - (y4 * x1))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 4)
    cv2.putText(frame, f'{int(tong_area/area_1*100)}%', (400, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    return frame

def detect_orange_object(frame):
    # Chuyển đổi khung hình từ BRG sang HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Định nghĩ phạm vi màu cam trong không gian màu HSV 
    lower = np.array([5, 100, 100])
    upper = np.array([10, 255, 255])

    # Tạo một mặt nạ nhị phân trong phạm vi đã định nghĩa 
    gray = cv2.inRange(hsv, lower, upper)
    cv2.imshow("gray", gray)

    # Tìm các đường viền (contours) trong mặt nạ
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for ct in contours:
        # Tính diện tích đường viền 
        area = cv2.contourArea(ct)
        
        # Nếu diện tích lớn hơn 2000, coi đây là đối tượng màu cam
        if area > 2000:
            approx = cv2.approxPolyDP(ct, 0.01 * cv2.arcLength(ct, True), True)     # Hàm Approximating contour để giảm số lượng điểm, làm cho đường viền mượt mà hơn
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)

            # Lấy tọa độ của điểm đầu tiên trong đường viền xấp xỉ 
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            cv2.putText(frame, 'orange', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def main():
    #cap = cv2.VideoCapture(0)

    while True:
        #ret, frame = cap.read()
        frame = cv2.imread("ke2.jpg",1)
        orange_object = detect_orange_object(frame)
        color_object = detect_color_object(orange_object)
        cv2.imshow('Orange',color_object)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()