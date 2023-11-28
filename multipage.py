import flet as ft
from flet import View, Page, AppBar, ElevatedButton, Text
from flet import RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment

# Import TimeTrackingApp class (ensure it's defined in the same module or imported properly)
from main_tracker import TimeTrackingApp
from Hours_calculation import TimeEntryProcessor


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
            page.views.append(
                View(
                    route='/time-tracking',
                    controls=[
                        AppBar(title=Text('Time Tracking'), bgcolor='blue'),
                        time_tracking_app,
                        ElevatedButton(text='Go Back', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                )
            )

        # Store
        elif page.route == '/calculate':
            page.views.append(
                View(
                    route='/calculate',
                    controls=[
                        AppBar(title=Text('Hours Calculations'), bgcolor='blue'),
                        Text(value='Hours Calculation', size=30),
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
