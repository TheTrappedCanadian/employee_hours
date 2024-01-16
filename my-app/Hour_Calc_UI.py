import flet as ft
from Hours_calculation import TimeEntryProcessor

def main(page: ft.Page):
    page.title = "Time Entry Analysis"

    # Create an instance of TimeEntryProcessor and process the data
    processor = TimeEntryProcessor('time_entries.json')
    processor.process_entries()
    detailed_data, total_hours = processor.get_processed_data()

    # UI Elements to display the processed data
    detailed_view = ft.ListView(expand=1)
    total_hours_view = ft.ListView(expand=1)

    # Populate the detailed_view with the detailed data
    for entry in detailed_data:
        detailed_view.controls.append(
            ft.ListTile(
                title=ft.Text(f"{entry['name']} - {entry['day']}"),
                subtitle=ft.Text(f"Time In: {entry['time_in']}, Time Out: {entry['time_out']}, Hours Worked: {entry['hours_worked']}")
            )
        )

    # Populate the total_hours_view with the total hours data
    for name, hours in total_hours.items():
        total_hours_view.controls.append(
            ft.ListTile(
                title=ft.Text(f"{name}"),
                subtitle=ft.Text(f"Total Hours: {hours:.2f}")
            )
        )

    # Add views to the page
    page.add(ft.Column([ft.Text("Detailed Time Entries", size=20), detailed_view]))
    # page.add(ft.Column([ft.Text("Total Hours Per Person", size=20), total_hours_view]))

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
