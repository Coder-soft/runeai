import customtkinter as ctk
import requests,webbrowser,os,subprocess,threading,pyautogui
from PIL import ImageGrab,Image
import tkinter as tk
from tkinter import filedialog
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
app=ctk.CTk()

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
def process_command(command):
    command=command.lower()
    if "download" in command:
        url=command.split("download ")[-1]
        return download_file(url)
    elif "search" in command:
        query=command.split("search ")[-1]
        return search_web(query)
    elif "uninstall" in command:
        app_name=command.split("uninstall ")[-1]
        return uninstall_app(app_name)
    elif "open" in command:
        resource=command.split("open ")[-1]
        return open_resource(resource)
    elif "volume" in command:
        level=int(command.split("volume ")[-1])
        return adjust_volume(level)
    elif "brightness" in command:
        level=int(command.split("brightness ")[-1])
        return adjust_brightness(level)
    elif "wifi" in command:
        state=command.split("wifi ")[-1]
        return toggle_wifi(state)
    elif "weather" in command:
        city_name=command.split("weather ")[-1]
        return get_weather(city_name)
    elif "screenshot" in command:
        capture_screenshot()
        return "Screenshot captured."
    else:return "Command not recognized. Please try again."
def send_message(event=None):
    user_input=chat_input.get()
    chat_log.insert(ctk.END,f"You: {user_input}\n")
    chat_input.delete(0,ctk.END)
    threading.Thread(target=handle_command,args=(user_input,)).start()
def show_commands():
    commands=("Available commands:\n- download [direct file link]\n- search [query]\n- uninstall [software name]\n- open [file or URL]\n- volume [0-100]\n- brightness [0-100]\n- wifi [on/off]\n- weather [city name]\n- screenshot [Currently In Development] ")
    chat_log.insert(ctk.END,f"RuneAI: {commands}\n")
import re
def format_response(response):
    response=response.replace("<b>","").replace("</b>","")
    response=response.replace("<br>","\n")
    response=response.replace("<a href='","URL:")
    response=response.replace("'>Click Here to Open Link</a>","")
    response=response.replace("'","")
    return response
import tkinter as tk
import customtkinter as ctk
import webbrowser
import re
def handle_command(user_input):
    response=process_command(user_input)
    formatted_response=format_response(response)
    chat_log.delete("1.0",tk.END)
    chat_log.insert(tk.END,f"RuneAI: {formatted_response}\n")
    link_pattern=re.compile(r"http[^\s]+")
    for match in link_pattern.finditer(formatted_response):
        link=match.group(0)
        start_index=chat_log.search(link,'1.0',tk.END)
        if start_index:
            end_index=f"{start_index}+{len(link)}c"
            chat_log.tag_add(link,start_index,end_index)
            chat_log.tag_configure(link,foreground="blue",underline=True)
            chat_log.tag_bind(link,"<Button-1>",lambda e,l=link:webbrowser.open(l))
def send_message(event=None):
    user_input=chat_input.get()
    chat_log.insert(tk.END,f"You: {user_input}\n")
    chat_input.delete(0,tk.END)
    threading.Thread(target=handle_command,args=(user_input,)).start()
def show_commands():
    commands=("Available commands:\n- download [direct file link]\n- search [query]\n- uninstall [software name]\n- open [file or URL]\n- volume [0-100]\n- brightness [0-100]\n- wifi [on/off]\n- weather [city name]\n- screenshot [Currently In Development] ")
    chat_log.insert(tk.END,f"RuneAI: {commands}\n")
app=ctk.CTk()
app.title("System Controller")
app.geometry("500x600")
chat_log=tk.Text(app,width=60,height=20,wrap='word')
chat_log.pack(pady=10)
input_frame=ctk.CTkFrame(app)
input_frame.pack(fill="x",padx=10,pady=10)
send_button=ctk.CTkButton(input_frame,text="→",width=50,command=send_message)
send_button.pack(side="left",padx=(0,10))
chat_input=ctk.CTkEntry(input_frame,placeholder_text="Type your message here...")
chat_input.pack(side="left",fill="x",expand=True)
commands_button=ctk.CTkButton(app,text="Show Commands",command=show_commands)
commands_button.pack(pady=10)
app.bind('<Return>',send_message)
app.mainloop()