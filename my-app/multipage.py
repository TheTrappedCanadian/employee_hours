import flet as ft
import requests
import json
from flet import View, Page, AppBar, ElevatedButton, Text, DataTable
from flet import RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment

# Import TimeTrackingApp class (ensure it's defined in the same module or imported properly)
from main_tracker import TimeTrackingApp
from Hours_calculation import TimeEntryProcessor
from send_to_cloud import send_to_cloud



def calculate_hours(e, results_area):
    processor = TimeEntryProcessor('time_entries.json')
    processor.process_entries()
    detailed_data, _ = processor.get_processed_data()

    # Clear the previous results
    results_area.controls.clear()

    # Add header row
    header_row = ft.Row([
        ft.Text("Name", width=100),
        ft.Text("Day", width=100),
        ft.Text("Time In", width=100),
        ft.Text("Time Out", width=100),
        ft.Text("Hours Worked", width=100)
    ])
    results_area.controls.append(header_row)

    # Add data rows
    for entry in detailed_data:
        row = ft.Row([
            ft.Text(entry['name'], width=100),
            ft.Text(entry['day'], width=100),
            ft.Text(entry['time_in'], width=100),
            ft.Text(entry['time_out'], width=100),
            ft.Text(entry['hours_worked'], width=100)
        ])
        results_area.controls.append(row)

    results_area.update()


def main(page: Page) -> None:
    page.title = 'Time Entry'


    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        # Home
        if page.route == '/':
            page.views.append(
                View(
                    route='/',
                    controls=[
                        AppBar(title=Text('Home'), bgcolor='blue'),
                        Text(value='Time Entry', size=30),
                        ElevatedButton(text='Go to Time Tracking', on_click=lambda _: page.go('/time-tracking')),
                        ElevatedButton(text='Calculate Hours', on_click=lambda _: page.go('/calculate'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )

        # Time Tracking
        elif page.route == '/time-tracking':
            time_tracking_app = TimeTrackingApp()
            scrollable_container = ft.Column(height=500, controls=[time_tracking_app])

            page.views.append(
                View(
                    route='/time-tracking',
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        AppBar(title=Text('Time Tracking'), bgcolor='blue'),
                        # scrollable_container,
                        time_tracking_app,
                        ElevatedButton(text='Go Back', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )


        # elif page.route == '/calculate':
        #     calculate_button = ElevatedButton(text='Calculate Hours', on_click=lambda e: calculate_hours(e, results_area))
        #     results_area = ft.Column()  # This will hold our "table" rows
        #
        #     page.views.append(
        #         View(
        #             route='/calculate',
        #             controls=[
        #                 AppBar(title=Text('Hours Calculations'), bgcolor='blue'),
        #                 calculate_button,
        #                 results_area,
        #                 ElevatedButton(text='Go Back', on_click=lambda _: page.go('/'))
        #             ],
        #             vertical_alignment=MainAxisAlignment.CENTER,
        #             horizontal_alignment=CrossAxisAlignment.CENTER,
        #             spacing=26
        #         )
        #     )

        # # ... [rest of your code] ...

        elif page.route == '/calculate':
            calculate_button = ElevatedButton(text='Calculate Hours', on_click=lambda e: calculate_hours(e, results_area))
            send_to_cloud_button = ElevatedButton(text='Send to Cloud', on_click=lambda e: send_to_cloud(e))
            results_area = ft.Column()  # This will hold our "table" rows

            page.views.append(
                View(
                    route='/calculate',
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        AppBar(title=Text('Hours Calculations'), bgcolor='blue'),
                        calculate_button,
                        send_to_cloud_button,
                        results_area,
                        ElevatedButton(text='Go Back', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )


        page.update()

    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == '__main__':
    ft.app(target=main)
