import requests
from bs4 import BeautifulSoup
from tkinter import *
from functools import partial
import re
from threading import Thread
from queue import Queue
from time import sleep
import json
import os

class ElementScraper:
    def __init__(self):
        self.base_url = "https://en.wikipedia.org"
        self.cache_file = "element_cache.json"
        self.element_data = {}
        self.queue = Queue()
        
    def fetch_element_data(self, element_url):
        """Scrape data for a single element"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(element_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get basic info
            name = soup.find('h1', {'id': 'firstHeading'}).text.strip()
            
            # Get atomic number
            atomic_num = soup.find('th', text=re.compile(r'Atomic number', re.I))
            atomic_num = atomic_num.find_next('td').text.strip() if atomic_num else "1"
            
            # Get symbol
            symbol = soup.find('th', text=re.compile(r'Symbol', re.I))
            symbol = symbol.find_next('td').text.strip() if symbol else name[:2]
            
            # Get category/group
            category = soup.find('th', text=re.compile(r'Group', re.I))
            category = category.find_next('td').text.strip() if category else "Unknown"
            
            # Get description from first paragraph
            description = ""
            intro = soup.find('div', {'class': 'mw-parser-output'}).find('p', recursive=False)
            if intro:
                description = intro.text.strip()
            
            # Clean data
            atomic_num = re.sub(r'\D', '', atomic_num) or "1"
            
            return {
                'atomic_number': atomic_num,
                'name': name,
                'symbol': symbol,
                'category': category,
                'description': description,
                'url': element_url
            }
            
        except Exception as e:
            print(f"Error scraping {element_url}: {str(e)}")
            return None

    def get_all_elements(self):
        """Get Wikipedia links for all elements"""
        periodic_table_url = f"{self.base_url}/wiki/Periodic_table"
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(periodic_table_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            elements = []
            for a in soup.select('table.wikitable a[href^="/wiki/"]:not([href*=":"])'):
                title = a.get('title', '')
                if '(' not in title and 'periodic table' not in title.lower():
                    elements.append({
                        'name': title,
                        'url': self.base_url + a['href']
                    })
            
            # Deduplicate
            seen = set()
            return [elem for elem in elements if not (elem['url'] in seen or seen.add(elem['url']))]
            
        except Exception as e:
            print(f"Error getting element list: {str(e)}")
            return []

    def worker(self):
        """Thread worker for scraping"""
        while True:
            element = self.queue.get()
            if element is None:
                break
                
            data = self.fetch_element_data(element['url'])
            if data:
                self.element_data[data['atomic_number']] = data
                self.save_cache()
                
            sleep(1)  # Be polite
            self.queue.task_done()

    def scrape_elements(self):
        """Scrape all elements with threading"""
        if os.path.exists(self.cache_file):
            self.load_cache()
            return
            
        elements = self.get_all_elements()
        print(f"Found {len(elements)} elements to scrape")
        
        # Start worker threads
        threads = []
        for _ in range(3):  # 3 threads
            t = Thread(target=self.worker)
            t.start()
            threads.append(t)
        
        # Add elements to queue
        for elem in elements:
            self.queue.put(elem)
        
        self.queue.join()
        
        # Stop workers
        for _ in range(3):
            self.queue.put(None)
        for t in threads:
            t.join()

    def save_cache(self):
        """Save scraped data to cache file"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.element_data, f)

    def load_cache(self):
        """Load scraped data from cache file"""
        with open(self.cache_file, 'r') as f:
            self.element_data = json.load(f)

class PeriodicTableApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.title("Modern Periodic Table (Web Scraped)")
        
        # Initialize scraper
        self.scraper = ElementScraper()
        
        # Start scraping in background
        Thread(target=self.scraper.scrape_elements, daemon=True).start()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main label
        Label(self.root, text='Modern Periodic Table', 
              font=("Arial Bold", 40), fg='black').pack()
        
        # Element groups frame
        self.create_element_groups_frame()
        
        # Periodic table elements
        self.create_periodic_elements()
        
        # Lanthanoids and Actinoids
        self.create_lanthanoids_actinoids()
        
        # Exit button
        Button(self.root, text="EXIT", height=4, width=7, bg='red', 
               command=self.root.destroy).pack(side='bottom')
    
    def get_category_color(self, category):
        """Map element categories to colors"""
        category = category.lower()
        if 'alkali metal' in category: return '#F08080'
        if 'alkaline earth' in category: return '#FFA500'
        if 'lanthanide' in category: return '#7F7FFF'
        if 'actinide' in category: return '#5FAFD7'
        if 'transition metal' in category: return '#BFEFFF'
        if 'post-transition' in category: return '#EEDFCC'
        if 'metalloid' in category: return '#FFFF00'
        if 'nonmetal' in category: return '#308014'
        if 'halogen' in category: return '#FFBBFF'
        if 'noble gas' in category: return '#00C957'
        return '#CCCCCC'  # Default color
    
    def create_element_groups_frame(self):
        """Create the frame with element group buttons"""
        group_frame = Frame(self.root, highlightbackground='black', highlightthickness=1)
        group_frame.place(x=600, y=92)
        
        groups = [
            ('Alkali metals', '#F08080'),
            ('Alkaline earth metals', '#FFA500'),
            ('Lanthanides', '#7F7FFF'),
            ('Actinides', '#5FAFD7'),
            ('Transition metals', '#BFEFFF'),
            ('Post-Transition metals', '#EEDFCC'),
            ('Metalloids', '#FFFF00'),
            ('Non-metals', '#308014'),
            ('Halogens', '#FFBBFF'),
            ('Noble gases', '#00C957')
        ]
        
        for i, (text, color) in enumerate(groups):
            row = (i // 2) + 1
            col = (i % 2) + 1
            Button(group_frame, text=text, bg=color, font=("Arial Bold", 9), 
                  height=2, width=25, command=partial(self.show_group_info, text)
                  ).grid(column=col, row=row)
    
    def create_periodic_elements(self):
        """Create all periodic table element buttons"""
        # Standard periodic table layout
        positions = [
            # Period 1
            (200, 100, '1'),   # H
            (1305, 100, '2'),  # He
            
            # Period 2
            (200, 166, '3'),   # Li
            (265, 166, '4'),   # Be
            (980, 166, '5'),   # B
            (1045, 166, '6'),  # C
            (1110, 166, '7'),  # N
            (1175, 166, '8'),  # O
            (1240, 166, '9'),  # F
            (1305, 166, '10'), # Ne
            
            # Period 3
            (200, 232, '11'),  # Na
            (265, 232, '12'),  # Mg
            (980, 232, '13'),  # Al
            (1045, 232, '14'), # Si
            (1110, 232, '15'), # P
            (1175, 232, '16'), # S
            (1240, 232, '17'), # Cl
            (1305, 232, '18'), # Ar
            
            # Period 4
            (200, 298, '19'),  # K
            (265, 298, '20'),  # Ca
            (330, 298, '21'),  # Sc
            (395, 298, '22'),  # Ti
            (460, 298, '23'),  # V
            (525, 298, '24'),  # Cr
            (590, 298, '25'),  # Mn
            (655, 298, '26'),  # Fe
            (720, 298, '27'),  # Co
            (785, 298, '28'),  # Ni
            (850, 298, '29'),  # Cu
            (915, 298, '30'),  # Zn
            (980, 298, '31'),  # Ga
            (1045, 298, '32'), # Ge
            (1110, 298, '33'), # As
            (1175, 298, '34'), # Se
            (1240, 298, '35'), # Br
            (1305, 298, '36'), # Kr
            
            # Period 5
            (200, 364, '37'),  # Rb
            (265, 364, '38'),  # Sr
            (330, 364, '39'),  # Y
            (395, 364, '40'),  # Zr
            (460, 364, '41'),  # Nb
            (525, 364, '42'),  # Mo
            (590, 364, '43'),  # Tc
            (655, 364, '44'),  # Ru
            (720, 364, '45'),  # Rh
            (785, 364, '46'),  # Pd
            (850, 364, '47'),  # Ag
            (915, 364, '48'),  # Cd
            (980, 364, '49'),  # In
            (1045, 364, '50'), # Sn
            (1110, 364, '51'), # Sb
            (1175, 364, '52'), # Te
            (1240, 364, '53'), # I
            (1305, 364, '54'), # Xe
            
            # Period 6
            (200, 430, '55'),  # Cs
            (265, 430, '56'),  # Ba
            (330, 430, '57'),  # La (placeholder)
            (395, 430, '72'),  # Hf
            (460, 430, '73'),  # Ta
            (525, 430, '74'),  # W
            (590, 430, '75'),  # Re
            (655, 430, '76'),  # Os
            (720, 430, '77'),  # Ir
            (785, 430, '78'),  # Pt
            (850, 430, '79'),  # Au
            (915, 430, '80'),  # Hg
            (980, 430, '81'),  # Tl
            (1045, 430, '82'), # Pb
            (1110, 430, '83'), # Bi
            (1175, 430, '84'), # Po
            (1240, 430, '85'), # At
            (1305, 430, '86'), # Rn
            
            # Period 7
            (200, 496, '87'),  # Fr
            (265, 496, '88'),  # Ra
            (330, 496, '89'),  # Ac (placeholder)
            (395, 496, '104'), # Rf
            (460, 496, '105'), # Db
            (525, 496, '106'), # Sg
            (590, 496, '107'), # Bh
            (655, 496, '108'), # Hs
            (720, 496, '109'), # Mt
            (785, 496, '110'), # Ds
            (850, 496, '111'), # Rg
            (915, 496, '112'), # Cn
            (980, 496, '113'), # Nh
            (1045, 496, '114'), # Fl
            (1110, 496, '115'), # Mc
            (1175, 496, '116'), # Lv
            (1240, 496, '117'), # Ts
            (1305, 496, '118')  # Og
        ]
        
        for x, y, atomic_num in positions:
            # Get element data from scraper (if available)
            element = self.scraper.element_data.get(atomic_num)
            
            if element:
                symbol = element['symbol']
                color = self.get_category_color(element['category'])
            else:
                # Fallback data if scraping isn't complete yet
                symbol = "?"
                color = '#CCCCCC'
            
            Button(self.root, text=symbol, bg=color, height=4, width=8,
                  command=partial(self.show_element_info, atomic_num)).place(x=x, y=y)
    
    def create_lanthanoids_actinoids(self):
        """Create lanthanoids and actinoids buttons"""
        # Lanthanoids (57-71)
        for i, atomic_num in enumerate(range(57, 72)):
            x = 330 + (i % 14) * 65
            y = 563
            
            element = self.scraper.element_data.get(str(atomic_num))
            if element:
                symbol = element['symbol']
                color = self.get_category_color(element['category'])
            else:
                symbol = "?"
                color = '#7F7FFF'
            
            Button(self.root, text=symbol, bg=color, height=4, width=8,
                  command=partial(self.show_element_info, str(atomic_num))).place(x=x, y=y)
        
        # Actinoids (89-103)
        for i, atomic_num in enumerate(range(89, 104)):
            x = 330 + (i % 14) * 65
            y = 630
            
            element = self.scraper.element_data.get(str(atomic_num))
            if element:
                symbol = element['symbol']
                color = self.get_category_color(element['category'])
            else:
                symbol = "?"
                color = '#5FAFD7'
            
            Button(self.root, text=symbol, bg=color, height=4, width=8,
                  command=partial(self.show_element_info, str(atomic_num))).place(x=x, y=y)
    
    def show_element_info(self, atomic_num):
        """Show information about a specific element"""
        info_window = Toplevel(self.root)
        info_window.geometry('400x500')
        info_window.maxsize(400, 600)
        
        element = self.scraper.element_data.get(str(atomic_num))
        
        if element:
            # Display element information
            Label(info_window, text=f"Atomic number: {atomic_num}", 
                  font=('Arial Bold', 12)).place(y=100)
            
            Label(info_window, text=element['symbol'], 
                  font=('Arial Bold', 35)).place(x=0)
            
            Label(info_window, text=element['name'], 
                  font=('Arial Bold', 12)).place(x=0, y=70)
            
            # Category and group info
            Label(info_window, text=f"Category: {element['category']}", 
                  font=('Arial Bold', 12)).place(y=130)
            
            # Description
            Message(info_window, text=element['description'], 
                   font=('Arial Bold', 12), width=400).pack(side='bottom')
            
            # Wikipedia link
            link = Label(info_window, text="Wikipedia Page", fg="blue", cursor="hand2",
                        font=('Arial Bold', 10))
            link.place(x=0, y=160)
            link.bind("<Button-1>", lambda e: self.open_url(element['url']))
        else:
            Label(info_window, text="Data not yet loaded...", 
                  font=('Arial Bold', 20), bg='#FF6347', width=300).place(x=0)
        
        # Back button
        Button(info_window, text='Back', font=("Arial Bold", 9), 
              width=10, relief="raised", command=info_window.destroy).place(x=320)
    
    def show_group_info(self, group_name):
        """Show information about an element group"""
        info_window = Toplevel(self.root)
        info_window.geometry('400x500')
        info_window.maxsize(400, 600)
        
        # Find elements in this group
        elements_in_group = []
        for atomic_num, element in self.scraper.element_data.items():
            if group_name.lower() in element['category'].lower():
                elements_in_group.append(element)
        
        if elements_in_group:
            # Display group name
            Message(info_window, text=group_name, font=('Arial Bold', 20),
                   bg='#F08080', width=300).place(x=0)
            
            # List elements in this group
            elements_text = "\n".join([f"{e['symbol']} - {e['name']}" for e in elements_in_group])
            Message(info_window, text=elements_text, font=('Arial Bold', 12), 
                   width=400).pack(side='bottom')
        else:
            Label(info_window, text=f"No {group_name} data loaded yet", 
                  font=('Arial Bold', 20), bg='#FF6347', width=300).place(x=0)
        
        # Back button
        Button(info_window, text='Back', font=("Arial Bold", 9), 
              width=10, relief="raised", command=info_window.destroy).place(x=320)
    
    def open_url(self, url):
        """Open a URL in default browser"""
        import webbrowser
        webbrowser.open_new(url)

def main():
    root = Tk()
    app = PeriodicTableApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()