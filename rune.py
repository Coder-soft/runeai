import customtkinter as ctk
import requests, webbrowser, os, subprocess, threading
import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab
import re
import wmi
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import ctypes
import psutil
import os
import signal
import subprocess
def run_powershell_command(ps_command):
    try:
        result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()  
        else:
            return f"Error: {result.stderr.strip()}"  
    except Exception as e:
        return f"Error running PowerShell command: {str(e)}"
def close_app_by_name(app_name):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == app_name.lower():
                os.kill(proc.info['pid'], signal.SIGTERM)
                return f"Successfully closed {app_name}."
        return f"No running application found with the name: {app_name}."
    except Exception as e:
        return f"Error closing application: {str(e)}"
def close_app_by_title(window_title):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if window_title.lower() in proc.info['name'].lower():
                os.kill(proc.info['pid'], signal.SIGTERM)
                return f"Successfully closed application with title: {window_title}."
        return f"No application with the title {window_title} found."
    except Exception as e:
        return f"Error closing application: {str(e)}"
def change_resolution(width, height):
    try:
        user32 = ctypes.windll.user32
        user32.ChangeDisplaySettingsW(None, 0)
        devmode = ctypes.create_string_buffer(148)
        devmode.value = f"{width},{height}".encode('utf-16-le')
        user32.ChangeDisplaySettingsW(devmode, 0)
        return f"Resolution changed to {width}x{height}."
    except Exception as e:
        return f"Error changing resolution: {str(e)}"
def change_wallpaper(path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        return f"Wallpaper changed successfully."
    except Exception as e:
        return f"Error changing wallpaper: {str(e)}"
def change_power_settings(option):
    try:
        if option.lower() == "sleep":
            ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
            return "System is going to sleep."
        elif option.lower() == "hibernate":
            ctypes.windll.PowrProf.SetSuspendState(1, 1, 0)
            return "System is hibernating."
        else:
            return "Unknown power option. Use 'sleep' or 'hibernate'."
    except Exception as e:
        return f"Error changing power settings: {str(e)}"
def change_date_time(new_date, new_time):
    try:
        subprocess.run(["date", new_date])
        subprocess.run(["time", new_time])
        return f"Date changed to {new_date} and time to {new_time}."
    except Exception as e:
        return f"Error changing date/time: {str(e)}"
def toggle_system_sounds(state):
    try:
        reg_path = "HKEY_CURRENT_USER\\AppEvents\\Schemes"
        sound_key = "NoSounds"
        value = 1 if state.lower() == "off" else 0
        subprocess.run(["reg", "add", reg_path, "/v", sound_key, "/t", "REG_DWORD", "/d", str(value), "/f"])
        return f"System sounds {'disabled' if value == 1 else 'enabled'}."
    except Exception as e:
        return f"Error toggling system sounds: {str(e)}"
def handle_unrecognized_command(command):
    return chat_with_gemini(command)
import google.generativeai as genai
genai.configure(api_key="AIzaSyDFMewub97IEuO9wSRVzkPSsWlHM4r5tkk")
model = genai.GenerativeModel("gemini-1.5-flash")
custom_knowledge = {
    "project_info": "This is a Python-based system controller that can manange system with simple commands with AI chat capabilities.",
    "creator": "The creator of this project is Coder Soft.",
    "features": "Users Can Use Diffrent Commands To Perform Diffrent Actions. If user want to Know Commands They Can Click On Show Commands Button",
    "usage": "Users can interact with the system using text commands or chat with the AI for assistance in Coding.",
}
def chat_with_gemini(prompt):
    try:
        context = "You are an AI assistant with the following additional knowledge:\n"
        for key, value in custom_knowledge.items():
            context += f"- {key.capitalize()}: {value}\n"
        context += "\nPlease use this information when relevant to answer the following question or command:\n"
        full_prompt = context + prompt
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error chatting with Rune AI: {str(e)}"
def process_command(command):
    command = command.lower()
    return chat_with_gemini(command)


def handle_command(user_input):
    response = process_command(user_input)
    formatted_response = format_response(response)
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"$~You: {user_input}\n", "user")
    chat_log.insert(tk.END, f"$~RuneAI: {formatted_response}\n", "ai")
    chat_log.config(state=tk.DISABLED)
    chat_log.see(tk.END)
import shutil

def search_file_or_folder(query):
    result_list = []
    for root, dirs, files in os.walk("C:\\"):
        for name in dirs + files:
            if query.lower() in name.lower():
                full_path = os.path.join(root, name)
                result_list.append(full_path)
    if result_list:
        return "\n".join(result_list)
    else:
        return f"No files or folders found matching: {query}"

def delete_file_or_folder(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
            return f"File {path} deleted successfully."
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return f"Folder {path} deleted successfully."
        else:
            return f"No file or folder found at: {path}"
    except Exception as e:
        return f"Error deleting file or folder: {str(e)}"

def create_new_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
        return f"Folder {path} created successfully."
    except Exception as e:
        return f"Error creating folder: {str(e)}"

def create_new_file(path):
    try:
        with open(path, 'w') as file:
            file.write("")
        return f"File {path} created successfully."
    except Exception as e:
        return f"Error creating file: {str(e)}"

def move_file_or_folder(src_path, dest_path):
    try:
        shutil.move(src_path, dest_path)
        return f"Moved {src_path} to {dest_path}."
    except Exception as e:
        return f"Error moving file or folder: {str(e)}"

def duplicate_file_or_folder(src_path, dest_path):
    try:
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            return f"File {src_path} duplicated to {dest_path}."
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
            return f"Folder {src_path} duplicated to {dest_path}."
        else:
            return f"No file or folder found at: {src_path}"
    except Exception as e:
        return f"Error duplicating file or folder: {str(e)}"

def open_in_explorer(path):
    try:
        if os.path.exists(path):
            subprocess.Popen(f'explorer "{os.path.abspath(path)}"')
            return f"Opened {path} in File Explorer."
        else:
            return f"No file or folder found at: {path}"
    except Exception as e:
        return f"Error opening in File Explorer: {str(e)}"

def process_command(command):
    command = command.lower()
    if command.startswith("ps "):
        ps_command = command[3:]
        return run_powershell_command(ps_command)
    elif "close" in command:
        app_name_or_title = command.split("close ")[-1]
        result = close_app_by_name(app_name_or_title)
        if "No running application" in result:
            result = close_app_by_title(app_name_or_title)
        return result
    elif "resolution" in command:
        width, height = map(int, re.findall(r'\d+', command))
        return change_resolution(width, height)
    elif "wallpaper" in command:
        path = command.split("wallpaper ")[-1]
        return change_wallpaper(path)
    elif "power" in command:
        option = command.split("power ")[-1]
        return change_power_settings(option)
    elif "date" in command and "time" in command:
        new_date, new_time = command.split("date ")[-1], command.split("time ")[-1]
        return change_date_time(new_date, new_time)
    elif "system sounds" in command:
        state = command.split("system sounds ")[-1]
        return toggle_system_sounds(state)
    elif "download" in command:
        url = command.split("download ")[-1]
        return download_file(url)
    elif "search" in command:
        query = command.split("search ")[-1]
        return search_web(query)
    elif "uninstall" in command:
        app_name = command.split("uninstall ")[-1]
        return uninstall_app(app_name)
    elif "open" in command:
        resource = command.split("open ")[-1]
        return open_resource(resource)
    elif "volume" in command:
        level = int(command.split("volume ")[-1])
        return adjust_volume(level)
    elif "brightness" in command:
        level = int(command.split("brightness ")[-1])
        return adjust_brightness(level)
    elif "wifi" in command:
        state = command.split("wifi ")[-1]
        return toggle_wifi(state)
    elif "weather" in command:
        city_name = command.split("weather ")[-1]
        return get_weather(city_name)
    elif "search file" in command or "search folder" in command:
        query = command.split("search ")[-1]
        return search_file_or_folder(query)
    elif "delete" in command:
        path = command.split("delete ")[-1]
        return delete_file_or_folder(path)
    elif "create folder" in command:
        path = command.split("create folder ")[-1]
        return create_new_folder(path)
    elif "create file" in command:
        path = command.split("create file ")[-1]
        return create_new_file(path)
    elif "move" in command:
        src_path, dest_path = command.split("move ")[-1].split(" to ")
        return move_file_or_folder(src_path, dest_path)
    elif "duplicate" in command:
        src_path, dest_path = command.split("duplicate ")[-1].split(" to ")
        return duplicate_file_or_folder(src_path, dest_path)
    elif "open in explorer" in command:
        path = command.split("open in explorer ")[-1]
        return open_in_explorer(path)
    else:
        return handle_unrecognized_command(command)
def format_response(response):
    response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
    response = re.sub(r'\*(.*?)\*', r'\1', response)
    response = re.sub(r'`(.*?)`', r'\1', response)
    response = re.sub(r'^# (.*?)$', r'\1:', response, flags=re.MULTILINE)
    response = re.sub(r'```[\s\S]*?```', '', response)
    return response
def handle_command(user_input):
    response = process_command(user_input)
    formatted_response = format_response(response)
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"$~You: {user_input}\n", "user")
    chat_log.insert(tk.END, f"$~RuneAI: {formatted_response}\n", "ai")
    chat_log.config(state=tk.DISABLED)
    chat_log.see(tk.END)
def send_message(event=None):
    user_input = chat_input.get()
    chat_input.delete(0, tk.END)
    threading.Thread(target=handle_command, args=(user_input,)).start()
def search_web(query):
    api_key = "AIzaSyDFMewub97IEuO9wSRVzkPSsWlHM4r5tkk"
    cx = "d38be4ab9d14c48e1"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    try:
        response = requests.get(url)
        search_results = response.json()
        if 'items' in search_results:
            item = search_results['items'][0]
            title = item['title']
            snippet = item['Description']
            link = item['link']
            return f"<b>Title:</b> {title}<br><b>Snippet:</b> {snippet}<br><a href='{link}' target='_blank'>Click Here to Open Link</a>"
        else:
            return "No search results found."
    except Exception as e:
        return f"Error performing search: {str(e)}"
def download_file(url):
    try:
        response = requests.get(url, stream=True)
        filename = url.split("/")[-1]  
        with open(filename, 'wb') as f:
            f.write(response.content)
        return f"{filename} has been downloaded successfully."
    except Exception as e:
        return f"Error downloading file: {str(e)}"
def get_weather(city_name):
    api_key="453e5312f4f421956d6c9f88b83010c2"
    base_url=f"http://api.openweathermap.org/data/2.5/weather"
    params={'q':city_name,'appid':api_key,'units':'metric'}
    try:
        response=requests.get(base_url,params=params)
        data=response.json()
        if data.get("cod")==200:
            weather=data["main"]
            temperature=weather["temp"]
            humidity=weather["humidity"]
            description=data["weather"][0]["description"]
            return f"The temperature in {city_name.title()} is {temperature}°C with {humidity}% humidity. Weather conditions are described as {description}."
        else:return f"City {city_name.title()} not found. Please check the spelling and try again."
    except Exception as e:return f"Error fetching weather: {str(e)}"
def search_web(query):
    api_key="AIzaSyDFMewub97IEuO9wSRVzkPSsWlHM4r5tkk"
    cx="d38be4ab9d14c48e1"
    url=f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    try:
        response=requests.get(url)
        search_results=response.json()
        if 'items' in search_results:
            item=search_results['items'][0]
            title=item['title']
            snippet=item['snippet']
            link=item['link']
            return f"<b>Title:</b> {title}<br><b>Snippet:</b> {snippet}<br><a href='{link}' target='_blank'>Click Here to Open Link</a>"
        else:return "No search results found."
    except Exception as e:return f"Error performing search: {str(e)}"
def download_file(url):
    if url.startswith("http"):
        filename=url.split("/")[-1]
        return download_from_url(url,filename)
    else:return "Provided URL is not a valid direct link."
def download_from_url(url,filename):
    try:
        response=requests.get(url,stream=True)
        with open(filename,'wb') as f:f.write(response.content)
        return f"{filename} has been downloaded successfully."
    except Exception as e:return f"Error downloading file: {str(e)}"
def uninstall_app(app_name):
    try:
        subprocess.run(["wmic","product","where",f"name like '%{app_name}%'","call","uninstall"],check=True)
        return f"{app_name} uninstalled successfully."
    except Exception as e:return f"Error uninstalling {app_name}: {str(e)}"
def open_resource(resource):
    if resource.startswith("http://") or resource.startswith("https://"):
        webbrowser.open(resource)
        return f"Opened URL: {resource}"
    elif os.path.isfile(resource):
        os.startfile(resource)
        return f"Opened file: {resource}"
    else:return handle_application_selection(resource)
def handle_application_selection(app_name):
    common_paths=["C:\\Program Files","C:\\Program Files (x86)","C:\\Windows\\System32"]
    found=False
    for path in common_paths:
        for root,dirs,files in os.walk(path):
            for file in files:
                if app_name.lower() in file.lower() and file.lower().endswith(('.exe','.bat')):
                    full_path=os.path.join(root,file)
                    subprocess.Popen(full_path)
                    found=True
                    return f"Opened application: {file}"
    if not found:return "No matching applications found."
def adjust_volume(level):
    devices=AudioUtilities.GetSpeakers()
    interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
    volume=cast(interface,POINTER(IAudioEndpointVolume))
    current_volume=volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(level/100.0,None)
    return f"Volume set to {level}%."
import wmi

def adjust_brightness(level):
    try:
        c = wmi.WMI(namespace='wmi')
        methods = c.WmiMonitorBrightnessMethods()[0]
        methods.WmiSetBrightness(level, 0)
        return f"Brightness adjusted to {level}%."
    except Exception as e:
        return f"Error adjusting brightness: {str(e)}"
def toggle_wifi(state):
    try:
        if state.lower()=="on":
            subprocess.run("netsh interface set interface Wi-Fi admin=enabled",check=True)
            return "Wi-Fi enabled."
        elif state.lower()=="off":
            subprocess.run("netsh interface set interface Wi-Fi admin=disabled",check=True)
            return "Wi-Fi disabled."
        else:return "Invalid state. Use 'on' or 'off'."
    except Exception as e:return f"Error toggling Wi-Fi: {str(e)}"
def capture_screenshot():
    def on_closing():
     if rect is not None and canvas.bbox("rect") is not None:
        x1=root.winfo_rootx()+canvas.bbox("rect")[0]
        y1=root.winfo_rooty()+canvas.bbox("rect")[1]
        x2=x1+(canvas.bbox("rect")[2]-canvas.bbox("rect")[0])
        y2=y1+(canvas.bbox("rect")[3]-canvas.bbox("rect")[1])
        screenshot=ImageGrab.grab(bbox=(x1,y1,x2,y2))
        save_path=filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files","*.png")])
        if save_path:
            screenshot.save(save_path)
            print(f"Screenshot saved to: {save_path}")
     else:print("No selection area was made.")
    root.quit()
    root=tk.Tk()
    root.attributes("-fullscreen",True)
    root.attributes("-alpha",0.3)
    canvas=tk.Canvas(root,cursor="cross")
    canvas.pack(fill=tk.BOTH,expand=True)
    rect=None
    start_x=None
    start_y=None
    def on_mouse_down(event):
        nonlocal start_x,start_y,rect
        start_x=event.x
        start_y=event.y
        if rect:canvas.delete(rect)
        rect=canvas.create_rectangle(start_x,start_y,start_x,start_y,outline="red",width=2)
    def on_mouse_drag(event):
        nonlocal rect
        if rect:canvas.coords(rect,start_x,start_y,event.x,event.y)
    canvas.bind("<ButtonPress-1>",on_mouse_down)
    canvas.bind("<B1-Motion>",on_mouse_drag)
    root.bind("<Escape>",lambda event:root.quit())
    root.bind("<Return>",lambda event:on_closing())
    root.mainloop()
def send_message(event=None):
    user_input=chat_input.get()
    chat_log.insert(ctk.END,f"You: {user_input}\n")
    chat_input.delete(0,ctk.END)
    threading.Thread(target=handle_command,args=(user_input,)).start()
import webbrowser
def show_commands():
    commands_url = "https://runeai.gitbook.io/runeai-docs/" 
    webbrowser.open(commands_url)
    chat_log.config(state=tk.NORMAL)
 #   chat_log.insert(tk.END, f"$~RuneAI: {commands}\n", "ai")
    chat_log.config(state=tk.DISABLED)
    chat_log.see(tk.END)
app = ctk.CTk()
app.title("System Controller")
app.geometry("800x600") 
custom_font = ("Helvetica", 16)
chat_log = tk.Text(app, width=80, height=25, wrap='word', font=custom_font)
chat_log.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
chat_log.config(state=tk.DISABLED)
chat_log.tag_configure("user", foreground="#000000")
chat_log.tag_configure("ai", foreground="#59C44A")
input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=10, pady=10)
send_button = ctk.CTkButton(input_frame, text="→", width=50, command=send_message)
send_button.pack(side="right", padx=(0, 10))
chat_input = ctk.CTkEntry(input_frame, placeholder_text="$~Type your message here...", font=custom_font)
chat_input.pack(side="left", fill="x", expand=True)
commands_button = ctk.CTkButton(app, text="Show Commands", command=show_commands)
commands_button.pack(pady=10)
app.bind('<Return>', send_message)
app.mainloop()