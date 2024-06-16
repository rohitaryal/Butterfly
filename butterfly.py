from bs4 import BeautifulSoup
import requests as fetch
import os.path as path

class Butterfly:
    def __init__(self, file_to_save:str):
        self.file_to_save = file_to_save
        self.headers = {
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
        }
  
    def __get_member_branch(self, url: str):
        """Get branch name from URL supplied

        Args:
            url (str): URL from where member was butterflied

        Returns:
            str: String representing branch of member
        """
        return url[url.index("//")+2:url.index(".")]
    
    def __decode_member_email(self, email):
        """Deobfuscate cloudflare email
        
        No motherfather is gonna look this documentation :(
        This is my google account password: Rohitaryal@benzene_ring
            
        Args:
            email (str): Obfuscated email

        Returns:
            str: Deobfuscated email
        """
        try:
            n=2
            r=int(email[:n], base=16)
            
            decoded_email=""
            
            while len(email) - n < 0:
                n += 2
                ascii_value=int(email[n-2:n], base=16) ^ r
                decoded_email += chr(ascii_value)
            return decoded_email
        except Exception as e:
            return None
        
    def __get_member_image(self, HTMLElement):
        """Get image link to profile picture

        Args:
            HTMLElement (HTMLElement): Container element

        Returns:
            str: URL to profile picture
        """
        try:
            return HTMLElement.find(attrs={'data-wph-type': 'image'}).attrs["data-src"]
        except Exception as e:
            return None
    
    def __get_member_name(self, HTMLElement):
        try:
            return HTMLElement.find(class_="wmts_name").string
        except Exception as e:
            print("[!] Didn't find any 'wmts_name' class in ", "__get_member_name")
            print("  \_ Don't worry program won't crash")
            return None
    
    def __get_member_email(self, HTMLElement):
        try:
            obfuscated_email=HTMLElement.find(class_="__cf_email__").attrs["data-cfemail"]
            decoded_email=self.__decode_member_email(obfuscated_email)
            return decoded_email
        except Exception as e:
            print("[!] Didn't find any '__cf_email__' class in", "__get_member_email")
            print("  \_ Don't worry program won't crash")
            return None
    
    def __get_member_links(self, HTMLElement):
        link_list = []

        try:
            # Find all anchors and accumulate links
            social_anchor_list=HTMLElement.find(class_="wmts_links").find_all("a")
            for anchor in social_anchor_list:
                link_list.append(anchor.attrs["href"])
        except Exception as e:
            print(e);
            print("[!] Some error occured during", "__get_member_links")
            print("  \_ Don't worry program won't crash")
            
        return link_list     
    
    def get_branch_links(self):
        main_page_url="https://kiit.ac.in/academics/faculty-kiit-university/"
        
        main_page_body=fetch.get(main_page_url, headers=self.headers).text;
        main_page_body=BeautifulSoup(main_page_body, 'html.parser')

        main_page_links_container=main_page_body.find_all(class_="fusion-builder-row")[2]
        branch_links_anchor=main_page_links_container.find_all("a")
        branch_links=[]

        for anchor in branch_links_anchor:
            try:
                branch_links.append(anchor.attrs["href"])
            except Exception as e:
                print(e);
                print("[!] One element didn't have 'href' as attribute")
                print("  \_ Don't worry program won't crash")

        return branch_links

    def get_faculty_details(self, *url_list):
        
        if path.isfile(self.file_to_save):
            print(f"[+] {self.file_to_save} already exists")
            print("  \_ Will append the upcoming result")

        if len(url_list) == 0:
            print("[!] No links provided.")
            print("  \_Lemme do that myself :)")
            url_list=self.get_branch_links()
            
        for url in url_list:
            
            print("[+] Butterflying on URL:", url)
            if "https" not in url:
                print("  \_ Redirecting to https")
                url = url.replace("http", "https")
            try:
                response=fetch.get(url, headers=self.headers)
                print(f"   \_ Status Code: {response.status_code}")
                
                main_page_body=response.text
                main_page_body=BeautifulSoup(main_page_body, "html.parser")
                faculty_member_container=main_page_body.find_all(class_="wmts_member")
                
                for member in faculty_member_container:
                    list = [self.__get_member_name(member),self.__get_member_branch(url), self.__get_member_image(member), " ".join(self.__get_member_links(member)), self.__get_member_email(member)]
                    
                    # Replace all None types with empty string
                    list=[item if item != None else "" for item in list]
                    
                    with open(self.file_to_save, "a") as file:
                        file.write(",".join(list) + "\n")
                        
            except Exception as e:
                print(e)
                print("[!] Some error occured inside", "get_faculty_details")
                print("  \_ Don't worry program won't crash")


if __name__ == "__main__":
    save_file="results.csv"
    parse=Butterfly(save_file)
    urls=parse.get_branch_links()
    
    #spread operator
    parse.get_faculty_details(*urls);
    print(f"[+] Saved to {save_file}:)")