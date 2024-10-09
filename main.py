import flet as ft
import os
import numpy as np
import base64

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from screeninfo import get_monitors
from time import sleep
from PIL import Image as image
from io import BytesIO
from file_set import *


monitor = get_monitors()

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument("--headless=new")
# chrome_options.add_argument(f"--window-size={monitor[0].width},{monitor[0].height}")
# chrome_options.add_argument(f"--window-size=1920,1080")
chrome_options.add_argument("--allow-file-access-from-files")


assets_dir = os.path.join(os.getcwd(), 'assets')
buff = BytesIO()

def main(page: ft.Page):
    def get_out_img():
        image_path = f'{assets_dir}\\screenshot.png'
        
        pil_photo = image.open(image_path)

        arr = np.asarray(pil_photo)
        pil_img = image.fromarray(arr)
        buff = BytesIO()
        pil_img.save(buff, format="PNG")

        newstring = base64.b64encode(buff.getvalue()).decode("utf-8")
        image_out.src_base64 = newstring

        page.update()
    
    def image_pick_event(e: ft.FilePickerResultEvent):
        photo_url.value = e.files[0].path
        page.update()
    
    def submit(e):
        page.open(open_progressed_dialog)

        download_page_with_css(url.value)
        pic_resize(photo_url.value)
        virtina_resize(assets_dir + '\\bg.png')
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        
        driver.get(f'file://{assets_dir}\\index.html')
        
        baner = driver.find_element(By.ID, "global_header")
        bg = driver.find_element(By.CLASS_NAME, "no_header.profile_page.has_profile_background")


        if vitrina_visible.value:
            try:
                right_col_element = driver.find_element(By.CLASS_NAME, 'screenshot_showcase_rightcol')
                driver.execute_script("arguments[0].remove();", right_col_element)

                driver.execute_script("""
                    var style = document.createElement('style');
                    style.innerHTML = ".screenshot_showcase_primary { width: 630px !important; max-width: none !important; }";
                    document.head.appendChild(style);
                """)

                vitrina = driver.find_element(By.CSS_SELECTOR, 'a.screenshot_showcase_screenshot.modalContentLink.ugc')

                img_element = vitrina.find_element(By.TAG_NAME, 'img')
                img_element_css = vitrina.find_element(By.CSS_SELECTOR, 'img')

            except Exception as e:
                vitrina = driver.find_element(By.CSS_SELECTOR, 'a.screenshot_showcase_screenshot.modalContentLink')

                img_element = vitrina.find_element(By.TAG_NAME, 'img')
                img_element_css = vitrina.find_element(By.CSS_SELECTOR, 'img')

            driver.execute_script("arguments[0].setAttribute('src', 'baner.png')", img_element)
            driver.execute_script("arguments[0].style.maxWidth = '630px';", img_element_css)
        

        driver.execute_script("""
        var baner = arguments[0];
        baner.parentNode.removeChild(baner);
        """, baner)
        driver.execute_script(f"""
        var bg = arguments[0];
        bg.style.backgroundImage = "url('bg.png')";
        """, bg)

        sleep(1)

        screenshot_path = f"{assets_dir}\\screenshot.png"
        driver.save_screenshot(screenshot_path)
        
        driver.quit()
        page.close(open_progressed_dialog)
        
        get_out_img()
        page.open(open_result_dialog)
  
    page.title = 'Steam BG chooser'
    page.theme = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed='indigo')
    
    file_picker = ft.FilePicker(on_result=image_pick_event)
    page.overlay.append(file_picker)
    
    image_out = ft.Image()

    url = ft.TextField(label="Enter profile URL", hint_text="https://steamcommunity.com/id/VerhovnaVlada/")
    photo = ft.ElevatedButton("Choose files...",
        on_click=lambda _: file_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE))
    photo_url = ft.TextField(label="Enter photo URL",)
    submit_but = ft.ElevatedButton("Submit", on_click=submit)
    vitrina_visible = ft.Checkbox(label="Is the window transparent?", value=False)
    
    open_progressed_dialog = ft.CupertinoAlertDialog(
                                content=ft.Column(
                                    [ft.ProgressRing(), ft.Text("In process...")],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                modal=True
                            )
    open_result_dialog = ft.AlertDialog(
                content=ft.Column(
                    [image_out],
                    # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                actions=[ft.TextButton("OK", on_click=lambda e: page.close(open_result_dialog))],
            )
    
    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        url,
                        ft.Row(
                            [
                                photo_url,
                                photo,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        vitrina_visible,
                        submit_but,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    
if __name__ == '__main__':
    ft.app(main)
