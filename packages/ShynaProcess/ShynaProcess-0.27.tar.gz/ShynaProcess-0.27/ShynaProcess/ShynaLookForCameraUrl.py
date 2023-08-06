import socket
import urllib.request
from ShynaDatabase import Shdatabase
from Shynatime import ShTime


class LookForCameraUrl:
    """
    Run update_cam_url function from the class. It will update the camera url in the database under cam_url table.
    it will automatically detect the router possible IP and then it tries to connect all possible devices.
    Cam return with data hence add that specific IP in the database.
    """
    base_ip = ""
    st_port = ":8080"
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()
    result = False
    cam_url = []

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0)
            try:
                # doesn't even have to be reachable
                s.connect(('10.255.255.255', 1))
                self.base_ip = s.getsockname()[0]
                # print(s.getsockname())
            except Exception as e:
                print(e)
                self.base_ip = '127.0.0.1'
            finally:
                s.close()
            return self.base_ip
        except Exception as e:
            print(e)

    def update_cam_url(self):
        try:
            self.base_ip = self.get_ip()
            self.base_ip = "http://" + str(self.base_ip).rsplit(".", maxsplit=1)[0] + "."
            for i in range(255):
                cam_url = str(self.base_ip) + str(i) + str(self.st_port)
                if self.open_url(ur=cam_url):
                    if self.check_existing_cam_url(ur=cam_url):
                        pass
                    else:
                        self.s_data.query = "INSERT INTO cam_url (cam_url,task_date,task_time,status)" \
                                            "VALUES('" + str(cam_url) + "','" + str(self.s_time.now_date) + "','" \
                                            + str(self.s_time.now_time) + "','active');"
                        self.s_data.insert_or_update_or_delete_with_status()
                else:
                    pass
        except Exception as e:
            print(e)

    def check_existing_cam_url(self, ur):
        try:
            self.result = False
            self.s_data.query = "Select cam_url from cam_url order by count DESC"
            base_ip = self.s_data.select_from_table()
            for item in base_ip:
                if ur in item:
                    self.result = True
        except Exception as e:
            print(e)
            self.result = False
        finally:
            return self.result

    def open_url(self, ur):
        try:
            x = urllib.request.urlopen(url=ur, timeout=2)
            response = x.read()
            if response == b'':
                self.result = False
            else:
                self.result = True
        except Exception:
            self.result = False
        finally:
            return self.result

    def get_cam_url(self):
        try:
            self.s_data.query = "Select cam_url from cam_url order by count DESC"
            base_ip = self.s_data.select_from_table()
            if base_ip[0] == 'Empty':
                self.cam_url.append(False)
            else:
                for item in base_ip:
                    for _ in item:
                        self.cam_url.append(_)
        except Exception as e:
            print(e)
            self.cam_url.append(False)
        finally:
            return self.cam_url
