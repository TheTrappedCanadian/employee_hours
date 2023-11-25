import flet as ft
import json
from datetime import datetime

class TimeTrackingApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.records = ft.Column()  # Initialize to None
        self.entry_data_list = []  # List to store entry data

    def build(self):
        self.name_field = ft.TextField(hint_text="Employee Name", width=200)
        self.day_field = ft.TextField(hint_text="Day (Monday)", width=200)
        self.time_in_field = ft.TextField(hint_text="Time In (HH:MM)", width=200)
        self.time_out_field = ft.TextField(hint_text="Time Out (HH:MM)", width=200)

        return ft.Column(
            width=800,
            controls=[
                ft.Row(
                    controls=[
                        self.name_field,
                        self.day_field,
                        self.time_in_field,
                        self.time_out_field,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_entry),
                    ],
                ),
                self.records,
            ],
        )

    def rebuild_records(self):
        # Clear existing rows
        self.records.controls.clear()

        # Rebuild rows based on current data
        for entry_data in self.entry_data_list:
            self.create_time_entry(entry_data)


    def add_entry(self, e):
        if self.name_field.value.strip():
            entry_data = {
                'name': self.name_field.value,
                'day': self.day_field.value,
                'time_in': self.time_in_field.value,
                'time_out': self.time_out_field.value
            }
            self.entry_data_list.append(entry_data)  # Add to data list
            self.rebuild_records()  # Rebuild the records
            self.save_entries()
            self.update()


    def create_time_entry(self, entry_data):
        entry_row = ft.Row(
            controls=[
                ft.Text(entry_data['name'], width=200),
                ft.Text(entry_data['day'], width=200),
                ft.Text(entry_data['time_in'], width=200),
                ft.Text(entry_data['time_out'], width=200),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, entry=entry_data: self.delete_entry(entry))
            ]
        )
        self.records.controls.append(entry_row)

    def delete_entry(self, entry_data):
        # Remove the entry data from the list
        if entry_data in self.entry_data_list:
            self.entry_data_list.remove(entry_data)
            self.rebuild_records()  # Rebuild the records
            self.save_entries()
            self.update()
            self.save_entries()
            print('post save entries')
            self.update()
            print('post update entries')

    def save_entries(self):
        with open('time_entries.json', 'w') as file:
            json.dump(self.entry_data_list, file)


    def load_entries(self):
        try:
            with open('time_entries.json', 'r') as file:
                self.entry_data_list = json.load(file)
                for entry_data in self.entry_data_list:
                    self.create_time_entry(entry_data)
        except FileNotFoundError:
            print("time_entries.json file not found, loading with no initial entries.")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"An error occurred while loading entries: {e}")


def main(page: ft.Page):
    page.title = "Employee Time Tracking"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    app = TimeTrackingApp()
    app.load_entries()
    page.add(app)
    page.update()


ft.app(target=main)



