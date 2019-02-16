from PackageBuilder.Source.Acquire import Acquirer
import requests

class HTTP(Acquirer):

    def Run(self):
        self.label = "Downloading %s" % self.address

        # Open file for writing
        file = open(self.dest, "wb")
        
        # Make request to server
        response = requests.get(self.address, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            # Unknown size
            file.write(response.content)

        else:
            downloaded_length = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                downloaded_length += len(data)
                file.write(data)
                self.progress = float(downloaded_length) / float(total_length)

        self.progress = 1.0
        

    @staticmethod
    def Understands(address: str):
        return address.startswith("http://") or address.startswith("https://")