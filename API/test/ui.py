import tkinter as tk

def main():
    # สร้างหน้าต่างหลัก
    root = tk.Tk()
    root.title("หน้าต่างภาษาไทย")
    root.geometry("300x200")

    # ตั้งค่า font ที่รองรับภาษาไทย (TH Sarabun New)
    thai_font = ("TH Sarabun New", 16)

    # แสดงข้อความภาษาไทย
    label = tk.Label(root, text="สวัสดีชาวโลก", font=thai_font)
    label.pack(pady=20)

    # สร้างปุ่มเพื่อปิดโปรแกรม
    close_button = tk.Button(root, text="ปิด", font=thai_font, command=root.quit)
    close_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
