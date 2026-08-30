#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامه برنامه‌ریزی روزانه
Daily Planner Application
"""

import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional

class Task:
    """کلاس برای نمایش هر وظیفه/کار"""
    
    def __init__(self, title: str, description: str = "", 
                 priority: int = 2, completed: bool = False,
                 time_slot: str = ""):
        self.title = title
        self.description = description
        self.priority = priority  # 1: بالا، 2: متوسط، 3: پایین
        self.completed = completed
        self.time_slot = time_slot
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'completed': self.completed,
            'time_slot': self.time_slot,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 2),
            completed=data.get('completed', False),
            time_slot=data.get('time_slot', '')
        )
        task.created_at = data.get('created_at', datetime.now().isoformat())
        return task
    
    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        priority_map = {1: "🔴", 2: "🟡", 3: "🟢"}
        priority_symbol = priority_map.get(self.priority, "🟡")
        
        time_info = f"[{self.time_slot}] " if self.time_slot else ""
        desc_info = f" - {self.description}" if self.description else ""
        
        return f"{status} {priority_symbol} {time_info}{self.title}{desc_info}"


class DailyPlanner:
    """کلاس اصلی برنامه‌ریزی روزانه"""
    
    def __init__(self, filename: str = "planner_data.json"):
        self.filename = filename
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """بارگذاری داده‌ها از فایل"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {'days': {}}
    
    def save_data(self):
        """ذخیره داده‌ها در فایل"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_today_key(self) -> str:
        """دریافت کلید امروز"""
        return date.today().isoformat()
    
    def get_tasks_for_day(self, day_key: str) -> List[Task]:
        """دریافت لیست وظایف برای یک روز خاص"""
        if day_key not in self.data['days']:
            self.data['days'][day_key] = []
        
        return [Task.from_dict(t) for t in self.data['days'][day_key]]
    
    def add_task(self, title: str, description: str = "", 
                 priority: int = 2, time_slot: str = "", 
                 day_key: Optional[str] = None) -> Task:
        """افزودن وظیفه جدید"""
        if day_key is None:
            day_key = self.get_today_key()
        
        if day_key not in self.data['days']:
            self.data['days'][day_key] = []
        
        task = Task(title, description, priority, False, time_slot)
        self.data['days'][day_key].append(task.to_dict())
        self.save_data()
        return task
    
    def complete_task(self, task_index: int, day_key: Optional[str] = None) -> bool:
        """علامت‌گذاری وظیفه به عنوان انجام شده"""
        if day_key is None:
            day_key = self.get_today_key()
        
        if day_key not in self.data['days']:
            return False
        
        if 0 <= task_index < len(self.data['days'][day_key]):
            self.data['days'][day_key][task_index]['completed'] = True
            self.save_data()
            return True
        return False
    
    def delete_task(self, task_index: int, day_key: Optional[str] = None) -> bool:
        """حذف وظیفه"""
        if day_key is None:
            day_key = self.get_today_key()
        
        if day_key not in self.data['days']:
            return False
        
        if 0 <= task_index < len(self.data['days'][day_key]):
            del self.data['days'][day_key][task_index]
            self.save_data()
            return True
        return False
    
    def get_statistics(self, day_key: Optional[str] = None) -> Dict:
        """دریافت آمار"""
        if day_key is None:
            day_key = self.get_today_key()
        
        tasks = self.get_tasks_for_day(day_key)
        total = len(tasks)
        completed = sum(1 for t in tasks if t.completed)
        pending = total - completed
        
        priority_counts = {1: 0, 2: 0, 3: 0}
        for task in tasks:
            if not task.completed:
                priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'high_priority': priority_counts.get(1, 0),
            'medium_priority': priority_counts.get(2, 0),
            'low_priority': priority_counts.get(3, 0)
        }


def print_menu():
    """نمایش منو"""
    print("\n" + "=" * 50)
    print("📅 برنامه برنامه‌ریزی روزانه")
    print("=" * 50)
    print("1. ➕ افزودن وظیفه جدید")
    print("2. 📋 مشاهده وظایف امروز")
    print("3. ✅ علامت‌گذاری وظیفه به عنوان انجام شده")
    print("4. ❌ حذف وظیفه")
    print("5. 📊 مشاهده آمار")
    print("6. 📅 مشاهده وظایف تاریخ دیگر")
    print("7. 💾 ذخیره و خروج")
    print("=" * 50)


def get_priority_input() -> int:
    """دریافت ورودی اولویت"""
    while True:
        print("\nاولویت را انتخاب کنید:")
        print("1. 🔴 بالا (مهم)")
        print("2. 🟡 متوسط (عادی)")
        print("3. 🟢 پایین (کم‌اهمیت)")
        try:
            choice = int(input("انتخاب شما (1-3): "))
            if choice in [1, 2, 3]:
                return choice
            print("لطفاً عدد بین 1 تا 3 وارد کنید.")
        except ValueError:
            print("ورودی نامعتبر است!")


def main():
    """تابع اصلی برنامه"""
    planner = DailyPlanner()
    
    print("\n" + "🎉" * 25)
    print("به برنامه برنامه‌ریزی روزانه خوش آمدید!")
    print("🎉" * 25)
    
    while True:
        print_menu()
        
        try:
            choice = input("\nانتخاب شما: ").strip()
            
            if choice == '1':
                # افزودن وظیفه جدید
                print("\n--- افزودن وظیفه جدید ---")
                title = input("عنوان وظیفه: ").strip()
                if not title:
                    print("❌ عنوان نمی‌تواند خالی باشد!")
                    continue
                
                description = input("توضیحات (اختیاری): ").strip()
                priority = get_priority_input()
                
                time_slot = input("بازه زمانی (مثلاً 9:00-10:00، اختیاری): ").strip()
                
                task = planner.add_task(title, description, priority, time_slot)
                print(f"\n✅ وظیفه با موفقیت افزوده شد!")
                print(f"   {task}")
            
            elif choice == '2':
                # مشاهده وظایف امروز
                today = planner.get_today_key()
                tasks = planner.get_tasks_for_day(today)
                
                print(f"\n--- وظایف امروز ({today}) ---")
                
                if not tasks:
                    print("هیچ وظیفه‌ای برای امروز ثبت نشده است.")
                else:
                    # نمایش وظایف انجام نشده
                    pending = [t for t in tasks if not t.completed]
                    completed = [t for t in tasks if t.completed]
                    
                    if pending:
                        print("\n📌 وظایف در دست انجام:")
                        for i, task in enumerate(pending):
                            print(f"   {i}. {task}")
                    
                    if completed:
                        print("\n✅ وظایف انجام شده:")
                        for i, task in enumerate(completed):
                            print(f"   {i}. {task}")
                    
                    print(f"\nمجموع: {len(tasks)} وظیفه | "
                          f"انجام شده: {len(completed)} | "
                          f"در انتظار: {len(pending)}")
            
            elif choice == '3':
                # علامت‌گذاری وظیفه به عنوان انجام شده
                today = planner.get_today_key()
                tasks = planner.get_tasks_for_day(today)
                pending = [t for t in tasks if not t.completed]
                
                if not pending:
                    print("هیچ وظیفه‌ای برای انجام وجود ندارد!")
                    continue
                
                print("\nوظایف در دست انجام:")
                for i, task in enumerate(pending):
                    print(f"   {i}. {task}")
                
                try:
                    index = int(input("\nشماره وظیفه انجام شده: "))
                    if 0 <= index < len(pending):
                        # پیدا کردن ایندکس واقعی در لیست اصلی
                        real_index = tasks.index(pending[index])
                        if planner.complete_task(real_index):
                            print("✅ وظیفه به عنوان انجام شده علامت‌گذاری شد!")
                        else:
                            print("❌ خطا در انجام عملیات!")
                    else:
                        print("شماره وظیفه نامعتبر است!")
                except ValueError:
                    print("ورودی نامعتبر است!")
            
            elif choice == '4':
                # حذف وظیفه
                today = planner.get_today_key()
                tasks = planner.get_tasks_for_day(today)
                
                if not tasks:
                    print("هیچ وظیفه‌ای برای حذف وجود ندارد!")
                    continue
                
                print("\nلیست وظایف:")
                for i, task in enumerate(tasks):
                    print(f"   {i}. {task}")
                
                try:
                    index = int(input("\nشماره وظیفه برای حذف: "))
                    if 0 <= index < len(tasks):
                        if planner.delete_task(index):
                            print("✅ وظیفه با موفقیت حذف شد!")
                        else:
                            print("❌ خطا در حذف وظیفه!")
                    else:
                        print("شماره وظیفه نامعتبر است!")
                except ValueError:
                    print("ورودی نامعتبر است!")
            
            elif choice == '5':
                # مشاهده آمار
                stats = planner.get_statistics()
                today = planner.get_today_key()
                
                print(f"\n--- آمار روز {today} ---")
                print(f"📊 مجموع وظایف: {stats['total']}")
                print(f"✅ انجام شده: {stats['completed']}")
                print(f"⏳ در انتظار: {stats['pending']}")
                
                if stats['pending'] > 0:
                    print(f"\n📌 اولویت‌های باقی‌مانده:")
                    print(f"   🔴 بالا: {stats['high_priority']}")
                    print(f"   🟡 متوسط: {stats['medium_priority']}")
                    print(f"   🟢 پایین: {stats['low_priority']}")
                
                if stats['total'] > 0:
                    progress = (stats['completed'] / stats['total']) * 100
                    print(f"\n📈 پیشرفت روز: {progress:.1f}%")
            
            elif choice == '6':
                # مشاهده وظایف تاریخ دیگر
                date_input = input("تاریخ مورد نظر را وارد کنید (YYYY-MM-DD): ").strip()
                
                try:
                    datetime.strptime(date_input, '%Y-%m-%d')
                    tasks = planner.get_tasks_for_day(date_input)
                    
                    print(f"\n--- وظایف تاریخ {date_input} ---")
                    
                    if not tasks:
                        print("هیچ وظیفه‌ای برای این تاریخ ثبت نشده است.")
                    else:
                        for i, task in enumerate(tasks):
                            print(f"   {i}. {task}")
                        
                        completed = sum(1 for t in tasks if t.completed)
                        print(f"\nمجموع: {len(tasks)} | انجام شده: {completed}")
                
                except ValueError:
                    print("فرمت تاریخ نامعتبر است! لطفاً از فرمت YYYY-MM-DD استفاده کنید.")
            
            elif choice == '7':
                # ذخیره و خروج
                planner.save_data()
                print("\n💾 داده‌ها ذخیره شدند.")
                print("خداحافظ! 👋")
                break
            
            else:
                print("انتخاب نامعتبر است! لطفاً عدد بین 1 تا 7 وارد کنید.")
        
        except KeyboardInterrupt:
            print("\n\n💾 داده‌ها ذخیره شدند.")
            print("خداحافظ! 👋")
            break
        except Exception as e:
            print(f"\n❌ خطا: {e}")


if __name__ == "__main__":
    main()
