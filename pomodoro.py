import tkinter as tk
from tkinter import messagebox, ttk
import time
import threading
import winsound

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("뽀모도로 타이머")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.config(bg="#f5f5f5")
        
        # 기본 설정값
        self.pomodoro_time = 50 * 60  # 25분
        self.short_break_time = 10 * 60  # 5분
        self.long_break_time = 30 * 60  # 15분
        self.pomodoro_count = 0
        self.timer_running = False
        self.current_time_left = self.pomodoro_time
        self.timer_thread = None
        self.blinking = False
        self.blink_count = 0
        self.original_bg = "#f5f5f5"
        self.blink_bg = "#ff7f7f"  # 붉은 계열 배경색
        
        # UI 구성
        self.setup_ui()
    
    def setup_ui(self):
        # 타이틀 레이블
        title_frame = tk.Frame(self.root, bg=self.original_bg)
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="뽀모도로 타이머", font=("Arial", 18, "bold"), bg=self.original_bg)
        title_label.pack()
        
        # 타이머 표시 레이블
        self.time_display = tk.Label(self.root, text="50:00", font=("Arial", 48), bg=self.original_bg)
        self.time_display.pack(pady=10)
        
        # 상태 표시 레이블
        self.status_display = tk.Label(self.root, text="준비", font=("Arial", 12), bg=self.original_bg)
        self.status_display.pack(pady=5)
        
        # 버튼 프레임
        button_frame = tk.Frame(self.root, bg=self.original_bg)
        button_frame.pack(pady=20)
        
        # 시작/일시정지 버튼
        self.start_button = tk.Button(button_frame, text="시작", command=self.start_timer, 
                                     width=10, height=2, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.start_button.grid(row=0, column=0, padx=10)
        
        # 리셋 버튼
        self.reset_button = tk.Button(button_frame, text="리셋", command=self.reset_timer,
                                     width=10, height=2, bg="#f44336", fg="white", font=("Arial", 10, "bold"))
        self.reset_button.grid(row=0, column=1, padx=10)
        
        # 설정 프레임
        settings_frame = tk.Frame(self.root, bg=self.original_bg)
        settings_frame.pack(pady=10)
        
        # 설정 레이블들
        tk.Label(settings_frame, text="작업 시간(분):", bg=self.original_bg).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        tk.Label(settings_frame, text="짧은 휴식(분):", bg=self.original_bg).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        tk.Label(settings_frame, text="긴 휴식(분):", bg=self.original_bg).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        # 설정 입력 위젯들
        self.pomodoro_entry = ttk.Spinbox(settings_frame, from_=1, to=60, width=5)
        self.pomodoro_entry.insert(0, "25")
        self.pomodoro_entry.grid(row=0, column=1, padx=5, pady=2)
        
        self.short_break_entry = ttk.Spinbox(settings_frame, from_=1, to=30, width=5)
        self.short_break_entry.insert(0, "5")
        self.short_break_entry.grid(row=1, column=1, padx=5, pady=2)
        
        self.long_break_entry = ttk.Spinbox(settings_frame, from_=1, to=60, width=5)
        self.long_break_entry.insert(0, "15")
        self.long_break_entry.grid(row=2, column=1, padx=5, pady=2)
        
        # 설정 적용 버튼
        apply_button = tk.Button(settings_frame, text="적용", command=self.apply_settings,
                               bg="#2196F3", fg="white", font=("Arial", 9))
        apply_button.grid(row=1, column=2, padx=10, pady=2, rowspan=1)
        
    def format_time(self, seconds):
        """초를 MM:SS 형식으로 변환"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def start_timer(self):
        """타이머 시작 또는 일시정지"""
        if not self.timer_running:
            self.timer_running = True
            self.start_button.config(text="일시정지")
            
            # 별도의 스레드에서 타이머 실행
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()
        else:
            self.timer_running = False
            self.start_button.config(text="계속")
    
    def run_timer(self):
        """타이머 로직 실행"""
        while self.current_time_left > 0 and self.timer_running:
            mins, secs = divmod(self.current_time_left, 60)
            time_string = f"{mins:02d}:{secs:02d}"
            
            # GUI 업데이트는 메인 스레드에서만 가능
            self.root.after(0, lambda t=time_string: self.time_display.config(text=t))
            
            time.sleep(1)
            self.current_time_left -= 1
        
        # 타이머가 완료되면
        if self.current_time_left <= 0 and self.timer_running:
            self.timer_complete()
    
    def blink_background(self):
        """배경색 깜빡임 효과"""
        if self.blink_count >= 10:  # 5초간 깜빡임 (0.5초 간격으로 10번)
            self.blinking = False
            self.blink_count = 0
            self.set_bg_color(self.original_bg)
            return
        
        if self.blinking:
            current_bg = self.root.cget("bg")
            if current_bg == self.original_bg:
                self.set_bg_color(self.blink_bg)
            else:
                self.set_bg_color(self.original_bg)
            
            self.blink_count += 1
            self.root.after(500, self.blink_background)  # 0.5초마다 호출
    
    def set_bg_color(self, color):
        """모든 위젯의 배경색 변경"""
        self.root.config(bg=color)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) or isinstance(widget, tk.Label):
                widget.config(bg=color)
                
        # 프레임 내부의 Label 위젯도 변경
        for frame in [widget for widget in self.root.winfo_children() if isinstance(widget, tk.Frame)]:
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg=color)
    
    def timer_complete(self):
        """타이머 완료 시 동작"""
        self.timer_running = False
        
        # 비프음 재생
        winsound.Beep(1000, 1000)  # 주파수 1000Hz, 1초간 재생
        
        # 배경 깜빡임 시작
        self.blinking = True
        self.blink_background()
        
        # 현재 모드에 따른 다음 모드 설정
        if self.status_display.cget("text") == "작업 중":
            self.pomodoro_count += 1
            
            # 4번의 뽀모도로마다 긴 휴식
            if self.pomodoro_count % 4 == 0:
                self.current_time_left = self.long_break_time
                self.status_display.config(text="긴 휴식")
                messagebox.showinfo("뽀모도로 완료", "긴 휴식 시간입니다!")
            else:
                self.current_time_left = self.short_break_time
                self.status_display.config(text="짧은 휴식")
                messagebox.showinfo("뽀모도로 완료", "짧은 휴식 시간입니다!")
        else:  # 휴식이 끝나면 작업 모드로
            self.current_time_left = self.pomodoro_time
            self.status_display.config(text="작업 중")
            messagebox.showinfo("휴식 완료", "다시 작업할 시간입니다!")
        
        # 화면 업데이트
        self.time_display.config(text=self.format_time(self.current_time_left))
        self.start_button.config(text="시작")
    
    def reset_timer(self):
        """타이머 리셋"""
        self.timer_running = False
        self.blinking = False
        self.blink_count = 0
        self.set_bg_color(self.original_bg)
        self.pomodoro_count = 0
        self.current_time_left = self.pomodoro_time
        self.status_display.config(text="준비")
        self.time_display.config(text=self.format_time(self.current_time_left))
        self.start_button.config(text="시작")
    
    def apply_settings(self):
        """설정 값 적용"""
        try:
            self.pomodoro_time = int(self.pomodoro_entry.get()) * 60
            self.short_break_time = int(self.short_break_entry.get()) * 60
            self.long_break_time = int(self.long_break_entry.get()) * 60
            
            # 현재 실행 중이지 않을 때만 표시 업데이트
            if not self.timer_running:
                self.current_time_left = self.pomodoro_time
                self.time_display.config(text=self.format_time(self.current_time_left))
            
            messagebox.showinfo("설정 적용", "새로운 설정이 적용되었습니다.")
        except ValueError:
            messagebox.showerror("오류", "올바른 숫자를 입력하세요.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()