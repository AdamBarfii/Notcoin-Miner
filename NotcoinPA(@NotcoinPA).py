import customtkinter
import tkinter as tk
from selenium import webdriver
import re
from tkinter import messagebox

# Some Configs
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class Tools:
    def __init__(self, root):
        self.root = root
        self.webdriver_var = tk.StringVar()

    def open_browser(self, *args) -> None:
        link_to_open = self.link_entry.get()
        selected_webdriver = optionmenu.get()
        print(selected_webdriver)
        link_to_open = re.sub(r'tgWebAppPlatform=[^&]+', 'tgWebAppPlatform=ios', link_to_open)

        if not link_to_open:
            messagebox.showwarning("Input Error", "Please enter a link before clicking the button.")
            return

        try:
            self.execute_js_in_browser(link_to_open, selected_webdriver)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print("Exception traceback:", e)

    def execute_js_in_browser(self, link: str, selected_webdriver: str) -> None:
        js_code = """
        powerLimitForAutotap = 500
        countclicks = 34
        recharging = false
        skipClick = false

        let app_root = document.querySelector('div[class^="_root"]')
        let multipleClicks = 5
        if (multipleClicks === undefined || multipleClicks === null) { multipleClicks = 0; }

        async function click() {
            let cc = document.querySelectorAll('div[class^="_notcoin"]');
            let scoreElement = document.querySelector('div[class^="_scoreCurrent"]');
            let score = parseInt(scoreElement.textContent);

            try {
                let imrocket = document.querySelectorAll('img[class^="_root"]');
                imrocket[0][Object.keys(imrocket[0])[1]].onClick();
                recharging = false;
            } catch (error) {}

            for (let step = 0; step < countclicks; step++) {
                score = parseInt(scoreElement.textContent);

                if (skipClick) {
                    break;
                }

                if (recharging) {
                    if (score >= powerLimitForAutotap) {
                        recharging = false;
                    }
                    break;
                }

                if (score > multipleClicks*2) {
                    try {
                        await new Promise((resolve) => {
                            cc[0][Object.keys(cc[0])[1]].onTouchStart('');
                            setTimeout(resolve, 100);
                        });
                    } catch (error) {}
                } else {
                    recharging = true;
                    break;
                }
            }
        }

        setInterval(click, 500);

        function start() {
            skipClick = false;
        }

        function stop() {
            skipClick = true;
        }
        """
        if selected_webdriver == "Chrome":
            driver = webdriver.Chrome()
        elif selected_webdriver == "Firefox":
            driver = webdriver.Firefox()
        elif selected_webdriver == "Edge":
            driver = webdriver.Edge()
        else:
            messagebox.showwarning("WebDriver Error", "Invalid WebDriver selection.")
            return
        driver.get(link)
        driver.execute_script(js_code)


root = customtkinter.CTk()
root.geometry("350x300")
root.maxsize(350, 300)
root.minsize(350, 300)
root.title('NotCoinPA (@NotCoinPA)')
tool = Tools(root)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Thanks for using us!")
label.pack(pady=12, padx=10)

tool.link_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Paste your link here!")
tool.link_entry.pack(pady=12, padx=10)

optionmenu = customtkinter.CTkOptionMenu(master=frame, values=["Firefox", "Chrome", "Edge"])
optionmenu.set("Firefox")
optionmenu.pack(pady=12, padx=10)

enter_browser_button = customtkinter.CTkButton(master=frame, text='Enter to open browser', command=tool.open_browser)
enter_browser_button.pack(pady=15, padx=10)


root.iconbitmap(r'')
root.resizable(False, False)
root.mainloop()
