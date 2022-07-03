###########################################
#
# Script to pass headers & cookies along 
#            with HTTP request
#        using "requests" package
#
#                    by
#
#             Code Monkey King   
#
###########################################

# packages
import requests

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "ajs_anonymous_id=%224cf398f4-6bc1-4add-af43-fb8b2077426c%22; ajs_anonymous_id=%224cf398f4-6bc1-4add-af43-fb8b2077426c%22; _gac_UA-128559955-2=1.1622359155.Cj0KCQjw78yFBhCZARIsAOxgSx3yKgFfwue6ClYjVmEvjTckOeUikq6xvbOjca64Nrxg7F42NXZI7F0aAivCEALw_wcB; _gcl_aw=GCL.1622359157.Cj0KCQjw78yFBhCZARIsAOxgSx3yKgFfwue6ClYjVmEvjTckOeUikq6xvbOjca64Nrxg7F42NXZI7F0aAivCEALw_wcB; _lr_uf_-dgy8s6=d3649ad4-9243-4a25-bb01-485705c045a2; ajs_user_id=%22u_DKhybQy%22; _ga=GA1.2.196569418.1622430555; _gid=GA1.2.1234090123.1622430555; _pd_session=ovXw%2Bo30EdUT4aGfA2iTetYsy9MgjX%2F5wFV1VN4ZH1vNhdQOtRNvPVZsSK9JLTg%2BhPkocpDu7KU2BiYbC75LW4jO%2BR6axSKaJJ3MOgSDYIeaqELVkurYScKSHGDpX9U8oVv3e6ohHeodDn9B26Sqx3s3aXKI8bvmYkLcbBVvEPgJ8yOuJ%2FWnuL0wXR9at6MxhZyunIObhSuJw2Dj0NiM%2ByfegKlMM47e2Zt6qPGylZ6Z--iGYL8HO7CsFfj6SC--bf7sbhELmHYZll9e%2F9vgPg%3D%3D; _lr_hb_-dgy8s6%2Fpipedreamcom={%22heartbeat%22:1622430779504}; _lr_tabs_-dgy8s6%2Fpipedreamcom={%22sessionID%22:0%2C%22recordingID%22:%224-d82768a7-5b1f-4540-b21b-34c0bea30870%22%2C%22lastActivity%22:1622430791810}",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,ur;q=0.8",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
    }
    
url = 'https://en8cyj2qt9remvj.m.pipedream.net'    
response = requests.get(url, headers = headers)
print(response.text)    
    
    
