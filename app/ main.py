from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, content, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode('utf-8'))
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Aqui, você pode analisar o post_data para determinar qual ação tomar
        # Por exemplo, se for para /save_info ou /get_info, você trata cada caso
        
        if self.path == '/save_info':
            # Aqui, implemente a lógica para scraping e salvar no MongoDB
            response = {"message": "Informação salva com sucesso."}
            self._send_response(response, 200)
        
        elif self.path == '/get_info':
            # Aqui, implemente a lógica para buscar as informações no MongoDB
            response = {"data": "Dados do site."}
            self._send_response(response, 200)
        
        else:
            self._send_response({"error": "Endpoint não encontrado"}, 404)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
