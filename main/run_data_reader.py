import time 
from devices.device_module import DataReader


def run_datareader(reader: DataReader, interval: int=1, retry_delay: int= 5):
    while True:
        try:
            print(f'Connecting to {reader.name} reader...')
            reader.connect()

            if hasattr(reader, 'is_connected') and not reader.is_connected():
                raise Exception('Connection Failed')
            
            print('Connected successfully')

            while True:
                try:
                    data = reader.read_data()

                    if data is not None:
                        print('Data', data)

                    else:
                        print('Not data read')
                    
                    time.sleep(interval)

                except Exception as read_error:
                    print('Read error: ', read_error)
                    break; # reconnect
                
        except Exception as conn_error:
            print('Connection error: ', conn_error)

        finally:
            try:
                reader.disconnect()
            except:
                pass

            print(f'Retrying in {retry_delay} seconds...\n')
            time.sleep(retry_delay)


if __name__ == '__main__':
    from devices.serial_reader import SerialReader

    reader = SerialReader()
    run_datareader(reader)

        
    