# coding=utf-8
# coding=utf-8
import socket
import sys
import traceback
import time
import os
import struct
import binascii
from threading import Thread
from pymongo import MongoClient
import datetime

folderPath = "log"
filePath = folderPath + "/" + str(time.strftime("%Y-%m-%d")) + ".txt"

# client = MongoClient('mongodb://tuan:tuan@119.15.161.69/eos')
# client = MongoClient('mongodb://tuan:tuan@202.60.104.121/eos')
client = MongoClient('mongodb://tuan:tuan@localhost/eos')
db = client.eos

socket_connected = True

def main():
    start_server()


def start_server():

    host = "0.0.0.0"

    port = 1186  # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire

    log_input(host, 'port', "Socket created")

    print "1. Socket created"

    try:
        soc.bind((host, port))
    except:
        log_input(host, 'port', "Bind failed. Error : " + str(sys.exc_info()))
        print "Bind failed. Error", str(sys.exc_info())
        sys.exit()

    soc.listen(50)  # queue up to 50 requests

    log_input(host, 'port', "Socket now listening")

    print "2. Socket now listening"

    # infinite loop- do not reset for every requests
    data_logger_id = ''

    while True:
        is_connected = True

        connection, address = soc.accept()

        ip, port = str(address[0]), str(address[1])

        log_input(ip, port, "Connected with " + ip + ":" + port)

        print("3. Connected with ip = %s : %s" % (ip, port))


        try:
            print("4. client_thread with ip = %s : %s" % (ip, port))
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            log_input(ip, port, "Thread did not start.")
            traceback.print_exc()

    soc.close()


def client_thread(connection, ip, port, max_buffer_size=5120):
    is_active = True
    is_loggin = False

    client_input_data = ''

    while is_active:
        try:
            print("4.1 client_thread with is_active = %s" % is_active)
            print("4.1 client_thread with is_active = %s" % is_active)
            # client_input_data = receive_input(connection, ip, port, max_buffer_size)
            # client_input_data = --QUIT-- or LOGIN or Envisoft Send command to datalogger
            # Get data from data logger
            client_input = connection.recv(max_buffer_size)
            # data = client_input

            # print "4.1.1.1 Receive data from datalogger:", client_input, 'EOF'
            print '4.2 Received data from datalogger with data = ', repr(client_input)
            print("4.3 Received data from datalogger with hex data = %s" % binascii.hexlify(client_input))
            print("4.4 Received data len = %s" % len(client_input))

            log_input(ip, port, 'received ' + binascii.hexlify(client_input))
            log_input(ip, port, 'length %d' % len(client_input))

            unpacker = struct.Struct('>ii16shh32s32s')
            unpacked_data = unpacker.unpack(client_input)
            type_command = '--TODO ORTHER--'

            print "Client input len: ", len(client_input)

            if len(client_input) > 0:
                # print "Received data len > 0: true"
                try:
                    # unpacker = struct.Struct('>ii16shh 32s32s')
                    # i = integer (4), 16s = string (16), h = integer (2)
                    log_input(ip, port, 'unpacked:  %s' % (unpacked_data,))
                    print 'len(data) > 0', repr(unpacked_data)
                    print 'Received datalogger value :', unpacked_data
                    print 'Received datalogger value 1 = Header :', unpacked_data[0]
                    print 'Received datalogger value 2 = TransID:', unpacked_data[1]
                    print 'Received datalogger value 3 = LoggerID:', unpacked_data[2].decode("UTF-8").rstrip(
                        ' \t\r\n\0')
                    print 'Received datalogger value 4 = Command:', unpacked_data[3]
                    # print '4.1.3.2 Unpacked Value 5 = Data length:', unpacked_data[4]
                    # print '4.1.3.2 Unpacked Value 6 = Data:', unpacked_data[5].decode("UTF-8").rstrip(' \t\r\n\0')
                    # print '4.1.3.2 Unpacked Value 7 = Data:', unpacked_data[6]

                    intCommand = int(unpacked_data[3])

                    # print "Command = ", intCommand

                    if intCommand == 256:
                        # 'LOGIN'
                        print "Envisoft run Command: LOGIN"
                        type_command = 'LOGIN'
                    if intCommand == 512:
                        # Run command: LOGGER_REQUEST_TIME
                        type_command = 'LOGGER_REQUEST_TIME'
                    else:
                        print "Envisoft run Command: Run COMMAND"
                        type_command = 'COMMAND'

                except Exception as e:
                    type_command = '--QUIT--'
                    print "--QUIT--"
                    # print ("4.1.3.3 Failed to unpacker.unpack(data) with error: %s" + str(e))
            else:
                type_command = '--TODO ORTHER--'
                print '--TODO ORTHER--'
        except:
            is_active = False
            type_command = '--QUIT--'
            print "--QUIT-- Client is unauthenticated or closed"
            connection.close()

        if '--QUIT--' in type_command:
            log_input(ip, port, "Client is unauthenticated or closed")
            print "4.2 --QUIT-- Client is unauthenticated or closed"

            values = (4, 257, 1, 3)
            packer = struct.Struct('>ihbb')
            packed_data = packer.pack(*values)
            connection.sendall(packed_data)
            log_input(ip, port, "Connection " + ip + ":" + port + " closed")
            is_active = False
            # logout(ip, port)
            connection.close()
        elif 'LOGGER_REQUEST_TIME' in type_command:
            # Run command: LOGGER_REQUEST_TIME
            # type_command = 'LOGGER_REQUEST_TIME'
            log_input(ip, port, "Run command: LOGGER_REQUEST_TIME")
            print "Server received request time form client"
            now = datetime.datetime.now()

            tmp_logger_id = str(unpacked_data[2])
            tmp_trans_id = int(unpacked_data[1])

            PACKET_HEAD = 33
            CMD_SERVER_RESPONSE_TIME = 513
            DATA_LENGTH = 5
            # Header (4 byte), TransID (4 byte), LoggerID (16 byte), Command (2 byte), Data length (2 byte),	Data
            values = (PACKET_HEAD, tmp_trans_id, tmp_logger_id, CMD_SERVER_RESPONSE_TIME, DATA_LENGTH,
                      now.year - 2000, now.month, now.day, now.hour, now.minute)

            packer = struct.Struct('>i i 16s h h b b b b b')
            packed_data = packer.pack(*values)
            try:
                log_input(ip, port, 'send ' + binascii.hexlify(packed_data))
                print "Server send command to client with command = SERVER_RESPONSE_TIME"
                connection.sendall(packed_data)
                print "Envisoft Send command SERVER_RESPONSE_TIME to Datalogger: ok"
            except socket.error, e:
                print "Error sending SERVER_RESPONSE_TIME data: %s" % e
                connection.close()
                is_active = False
                break
        # End LOGGER_REQUEST_TIME
        else:
            # log_input(ip, port, "Processed result: {}".format(client_input_data))

            # print "Processed result: {}".format(client_input_data)

            if 'LOGIN' in type_command:
                tmp_logger_id = str(unpacked_data[2])
                tmp_trans_id = int(unpacked_data[1])
                now = datetime.datetime.now()
                # values = (25, tmp_trans_id, tmp_logger_id, 257, 1, 0)
                # values = (30, tmp_trans_id, tmp_logger_id, 257, 6, 0, now.year - 2000, now.month, now.day, now.hour, now.minute, now.second)
                values = (34, tmp_trans_id, tmp_logger_id, 257, 6, 0, now.year - 2000, now.month, now.day, now.hour, now.minute,
                now.second)
                # values = (34, tmp_trans_id, tmp_logger_id, 257, 6, 0, 19, 03, 24, 4, 43, 50)

                # Send: SERVER _LOGGING_STATUS
                # Header (4 byte), TransID (4 byte), LoggerID (16 byte), Command (2 byte), Data length (2 byte),	Data

                # packer = struct.Struct('>ihbb')
                packer = struct.Struct('>i i 16s h h b b b b b b b')
                # i = integer (4), 16s = string (16), h = integer (2), b = integer (1)
                packed_data = packer.pack(*values)

                try:
                    print("Envisoft start send login data = %s" % binascii.hexlify(packed_data))
                    if is_loggin != True:
                        connection.sendall(packed_data)
                        # wait for two seconds
                        time.sleep(2)
                        print "Envisoft start send login data: ok"
                        is_loggin = True
                    print "---------------------------------------"
                    print "5. Envisoft scan database to send command: after login ok"

                    tmp_logger_id = str(unpacked_data[2].decode("UTF-8").rstrip(' \t\r\n\0'))

                    tmp_trans_id = int(unpacked_data[1])

                    # Trint: Demo
                    demoAdjustment(connection, tmp_logger_id)

                    envisoft_send_command_to_datalogger(connection, ip, port, tmp_logger_id, tmp_trans_id,
                                                        max_buffer_size=5120)


                except socket.error, e:
                    print "Error sending loggin data: %s" % e
                    socket_conneted = False
                    connection.close()
                    is_active = False

            if 'COMMAND' in type_command:
                try:
                    print "---------------------------------------"
                    print "5. Envisoft scan database to send command"
                    tmp_logger_id = str(unpacked_data[2].decode("UTF-8").rstrip(' \t\r\n\0'))
                    tmp_trans_id = int(unpacked_data[1])

                    #Trint: Demo
                    demoAdjustment(connection, tmp_logger_id)

                    envisoft_send_command_to_datalogger(connection, ip, port, tmp_logger_id, tmp_trans_id,
                                                    max_buffer_size=5120)
                except Exception as e:
                    print ("Failed to unpacker.unpack(data) with error: %s" + str(e))
            else:
               print "To do nothing"

def demoAdjustment(connection, tmp_logger_id):
    print "---------------------------------------"
    if "DLV1.1-19030011" in tmp_logger_id:
        print "Call --> getAdjustmentTest --> SO2"
        getAdjustmentTest(connection, tmp_logger_id, "SO2")
        time.sleep(1)
        print "Call --> getAdjustmentTest --> CO2"
        getAdjustmentTest(connection, tmp_logger_id, "CO2")
        time.sleep(1)
        print "Call --> getAdjustmentTest --> NO"
        getAdjustmentTest(connection, tmp_logger_id, "NO")
        time.sleep(1)
        print "Call --> getAdjustmentTest --> CH4"
        getAdjustmentTest(connection, tmp_logger_id, "CH4")
        time.sleep(1)
    if "DLV1.1-19030007" in tmp_logger_id:
        getAdjustmentTest(connection, tmp_logger_id, "pH")
        time.sleep(1)
        getAdjustmentTest(connection, tmp_logger_id, "EC")
        time.sleep(1)
        getAdjustmentTest(connection, tmp_logger_id, "DO")
        time.sleep(1)
        getAdjustmentTest(connection, tmp_logger_id, "TSS")
        time.sleep(1)
        getAdjustmentTest(connection, tmp_logger_id, "TURB")
        time.sleep(1)
        getAdjustmentTest(connection, tmp_logger_id, "NO3")
        time.sleep(1)
        getAdjustmentTest(connection, tmp_logger_id, "Temp")
    if "DLV1.1-19030007-Formosa-Nuoc" in tmp_logger_id:
        # COD
        getAdjustmentTest(connection, tmp_logger_id, "COD")
        # SS
        getAdjustmentTest(connection, tmp_logger_id, "SS")
        # Temp
        getAdjustmentTest(connection, tmp_logger_id, "Temp")
        # Flow
        getAdjustmentTest(connection, tmp_logger_id, "Flow")
        # TN
        getAdjustmentTest(connection, tmp_logger_id, "TN")
        # Oil
        getAdjustmentTest(connection, tmp_logger_id, "Oil")
        # Xyanua
        getAdjustmentTest(connection, tmp_logger_id, "Xyanua")
        # Cd
        getAdjustmentTest(connection, tmp_logger_id, "Cd")
        # Cr6 +
        getAdjustmentTest(connection, tmp_logger_id, "Cr6 +")
        # Phenol
        getAdjustmentTest(connection, tmp_logger_id, "Phenol")
        # Hg
        getAdjustmentTest(connection, tmp_logger_id, "Hg")
        # Colour
        getAdjustmentTest(connection, tmp_logger_id, "Colour")
        # Fe
        getAdjustmentTest(connection, tmp_logger_id, "Fe")
        # Amoni
        getAdjustmentTest(connection, tmp_logger_id, "Amoni")

def getAdjustmentTest(connection, data_logger_id, indicator_name):
    try:
        print "---------------------------------"
        print("---->Server send adjustment command Logger id: indicator name =  %s : %s" % (data_logger_id, indicator_name))

        CMD_SERVER_SET_CALIB_TIME = 8192
        DATA_LENGTH = 0
        TRANS_ID = 10
        LOGGER_ID = data_logger_id

        max_record = 3
        data_length = 32
        data_length = data_length + (11*max_record)
        PACKET_HEADER = data_length + 28

        values = (PACKET_HEADER, TRANS_ID, LOGGER_ID, CMD_SERVER_SET_CALIB_TIME)
        values_list = list(values)

        format_data = ">i i 16s h h 32s"

        values_list.append(data_length)
        values_list.append(indicator_name)

        count = 0

        for x in range(max_record):
            now = datetime.datetime.now()
            values_list.append(1)
            now.month, now.day, now.hour, now.minute
            values_list.append(now.year - 2000)
            values_list.append(now.month)
            values_list.append(now.day)
            values_list.append(now.hour)
            values_list.append(now.minute)

            # wait for two seconds
            time.sleep(1)
            now = datetime.datetime.now()
            now.month, now.day, now.hour, now.minute
            values_list.append(now.year - 2000)
            values_list.append(now.month)
            values_list.append(now.day + count)
            values_list.append(now.hour)
            values_list.append(now.minute)

            format_data = format_data + " b b b b b b b b b b b"
            data_length = data_length + 11
            count = count + 1
            if count >= max_record:
                break
        values = tuple(values_list)
        print(values)
        print(format_data)

        packer = struct.Struct(format_data)
        packed_data = packer.pack(*values)

        print values
        print("Send Adjustment command = %s" % binascii.hexlify(packed_data))
        connection.sendall(packed_data)
        print "Send djustment command: OK"
    except:
        print "Adjustment command: Error", str(sys.exc_info())
        traceback.print_exc()


def envisoft_send_command_to_datalogger(connection, ip, port, logger_id, trans_id, max_buffer_size=5120):
    # time.sleep(6)
    logger_id = logger_id

    # is_active = getDataloggerStatus(ip, logger_id)

    print("6. Call -> envisoft_send_command_to_datalogger")

    there_are_commands = True

    log_input(ip, port, "client_command_thread " + ip + ":" + port)

    # while is_active:
    # while there_are_commands:
    while True:
        # print "------------------"
        try:
            command = getDataloggerCommand(ip, logger_id)

            if command:
                print "-----> Command"
                commandCode = str(command.get('title'))
                db_logger_id = str(command.get('logger_id'))
                commandData = str(command.get('command'))
                number_sample = int(command.get('bottle'))

                print("Envisoft sent command to datalogger: All = %s" % command)
                # print("Envisoft sent command to datalogger: Command = %s" % commandCode)
                # print("Logger id : commandCode : Command data = %s : %s : %s" % (db_logger_id, commandCode, commandData))
                print("Logger_Id = %s" % db_logger_id)
                print("command_Code = %s" % commandCode)
                print("command_Data = %s" % commandData)
                print("number_sample = %s" % number_sample)
                # commandCode = str(command.get('command_code'))

                log_input(ip, port, "client_command_thread " + ip + ":" + port + " command_code %s" % commandCode)

                values = ()
                packer = struct.Struct('>i i 16s h h')

                packed_data = ''

                if commandCode == 'SERVER_GET_INPUT_ALL':
                    # commandData = str(command.get('command_data'))
                    commandData = str(command.get('command'))

                    # print("Command data = %s" % command.get('command'))

                    # values = (24, 1, logger_id, 1, 0)
                    values = (24, trans_id, logger_id, 1, 0)

                    packer = struct.Struct('>i i 16s h h')
                    packed_data = packer.pack(*values)

                elif commandCode == 'SERVER_GET_INPUT_CHAN':
                    # commandData = str(command.get('command_data'))
                    commandData = str(command.get('command'))

                    # print("Command data = %s" % command.get('command'))

                    # values = (56, 2, logger_id, 3, 32, commandData)
                    values = (56, trans_id, logger_id, 3, 32, commandData)

                    packer = struct.Struct('>i i 16s h h 32s')
                    # Header (i = 4 byte), TransID (i = 4 byte), LoggerID (16s = 16 byte),
                    # Command (h = 2 byte), Data length (h = 2 byte),	Data
                    packed_data = packer.pack(*values)

                elif commandCode == 'SERVER_GET_SAMPLE':
                    # commandData = str(command.get('command_data'))
                    commandData = str(command.get('command'))
                    #number_sample = int(command.get('number_sample'))
                    number_sample = int(command.get('bottle'))

                    # print("Command data = %s" % command.get('command'))
                    # print("number_sample = %s" % command.get('bottle'))

                    # values = (57, 3, logger_id, 17, 33, commandData, number_sample)
                    values = (57, trans_id, logger_id, 17, 33, commandData, number_sample)

                    packer = struct.Struct('>i i 16s h h 32s b')
                    # Header (i = 4 byte), TransID (i = 4 byte), LoggerID (16s = 16 byte),
                    # Command (h = 2 byte), Data length (h = 2 byte),	Data
                    packed_data = packer.pack(*values)

                elif commandCode == 'SERVER_SET_CALIB_TIME':
                    commandData = str(command.get('command_data'))
                    number_sample = int(command.get('number_sample'))

                    # print("Command data = %s" % command.get('command_data'))
                    # print("number_sample = %s" % command.get('number_sample'))

                    # values = (456, 6, logger_id, 8192, 432, commandData, number_sample)
                    values = (456, trans_id, logger_id, 8192, 432, commandData, number_sample)
                    packer = struct.Struct('>i i 16s h h 32s b')
                    # Header (i = 4 byte), TransID (i = 4 byte), LoggerID (16s = 16 byte),
                    # Command (h = 2 byte), Data length (h = 2 byte),	Data
                    packed_data = packer.pack(*values)

                # else:
                #    values = (2, 1)
                #    packer = struct.Struct('>ih')
                #    packed_data = packer.pack(*values)

                # print("8. Command code = %s" % command.get('title'))
                # print("9. Command data = %s" % command.get('command'))

                log_input(ip, port, 'send ' + binascii.hexlify(packed_data))

                # print("10 Envisoft Send command to Datalogger with command = %s" % command.get('command'))
                connection.sendall(packed_data)
                print "Envisoft Send command to Datalogger: ok"
            else:
                print("There are no commands defined in the %s" % logger_id)
                # there_are_commands = False
            # time.sleep(5)
            adjustment = getDataloggerAdjustment(ip, logger_id)
            if adjustment:
                print "-->adjustment"
                print("Envisoft sent adjustment to datalogger: command = %s" % adjustment)
                command_code = str(adjustment.get('title'))
                command_data = str(adjustment.get('content'))
                indicator_name = str(adjustment.get('indicator_name'))
                from_date = str(adjustment.get('from_date'))
                to_date = str(adjustment.get('to_date'))
                db_logger_id = str(adjustment.get('logger_id'))

                print("Logger_Id = %s" % db_logger_id)
                print("command_Code = %s" % command_code)
                print("command_Data = %s" % command_data)
                print("from_date = %s" % from_date)
                print("to_date = %s" % to_date)

                now = datetime.datetime.now()
                print(now.year, now.month, now.day, now.hour, now.minute, now.second)

                datalogger_header = 456
                datalogger_Command = 8192
                datalogger_length = 432
                number_schedule = 1
                datalogger_command_id = 1

                # print("Command data = %s" % command.get('command_data'))
                # print("number_sample = %s" % command.get('number_sample'))

                # values = (456, 6, logger_id, 8192, 432, commandData, indicator_name, from_date,)
                values = (datalogger_header, trans_id, db_logger_id, datalogger_Command, datalogger_length, number_schedule,
                          datalogger_command_id, indicator_name,
                          now.year, now.month, now.day, now.hour, now.minute, now.second,
                          now.year, now.month, now.day, now.hour, now.minute, now.second)
                packer = struct.Struct('>i i 16s h h b b 32s B B B B B B B B B B B B')
                # Header (i = 4 byte), TransID (i = 4 byte), LoggerID (16s = 16 byte),
                # Command (h = 2 byte), Data length (h = 2 byte),	Data (32)
                packed_data = packer.pack(*values)

                log_input(ip, port, 'send ' + binascii.hexlify(packed_data))

                connection.sendall(packed_data)
                print "Envisoft send adjustment command to Datalogger: ok"
            else:
                print("There are no adjustment defined in the %s" % logger_id)
                # there_are_commands = False

            print "---------------------------------------"
            demoAdjustment(connection, logger_id)

        except:
            log_input(ip, 'port', "Bind failed. Error : " + str(sys.exc_info()))
            print "Bind failed. Error", str(sys.exc_info())

        there_are_commands = True
        time.sleep(5)
        # is_active = getDataloggerStatus(ip, logger_id)

def client_command_thread(connection, ip, port, client_input, max_buffer_size=5120):
    # time.sleep(6)
    unpacker = struct.Struct('>ii16shh32s32s')
    unpacked_data = unpacker.unpack(client_input)
    logger_id = str(unpacked_data[2])

    type_command = '--TODO ORTHER--'

    is_active = getDataloggerStatus(ip, logger_id)

    print "-------------------------------------------------"
    print("5.1 client_command_thread: is_active = %s" % is_active)

    log_input(ip, port, "client_command_thread " + ip + ":" + port + " start %d" % is_active)

    while is_active:
        command = getDataloggerCommand(ip, logger_id)

        if command:
            print("5.2 Envisoft sent command to datalogger: command = %s" % command)
            commandCode = str(command.get('command_code'))
            logger_id = str(command.get('logger_id'))
            log_input(ip, port, "client_command_thread " + ip + ":" + port + " command_code %s" % commandCode)
            print("5.3 commandCode = %s" % commandCode)

            values = ()
            packer = struct.Struct('>ih')

            packed_data = ''

            if commandCode == 'SERVER_GET_INPUT_ALL':
                values = (24, 1, logger_id, 1, 0)
                # TransID = tùy biến
                # Logger_id = tùy biến
                packer = struct.Struct('>i i 16s h h')
                packed_data = packer.pack(*values)
            elif commandCode == 'SERVER_GET_INPUT_CHAN':
                commandData = str(command.get('command_data'))
                print("Command data = %s" % command.get('command_data'))
                # values = (3, 3, commandData)
                values = (56, 2, logger_id, 3, 32, commandData)
                # packer = struct.Struct('>ihb')
                packer = struct.Struct('>i i 16s h h 32s')
                # Header (i = 4 byte), TransID (i = 4 byte), LoggerID (16s = 16 byte),
                # Command (h = 2 byte), Data length (h = 2 byte),	Data
                packed_data = packer.pack(*values)
            elif commandCode == 'SERVER_GET_SAMPLE':
                commandData = str(command.get('command_data'))
                print("Command data = %s" % command.get('command_data'))
                number_sample = int(command.get('number_sample'))
                print("number_sample = %s" % command.get('number_sample'))
                values = (57, 3, logger_id, 17, 33, commandData, number_sample)
                packer = struct.Struct('>i i 16s h h 32s b')
                # Header (i = 4 byte), TransID (i = 4 byte), LoggerID (16s = 16 byte),
                # Command (h = 2 byte), Data length (h = 2 byte),	Data
                packed_data = packer.pack(*values)

            elif commandCode == 'SERVER_SET_CALIB_TIME':
                commandData = str(command.get('command_data'))
                print("Command data = %s" % command.get('command_data'))
                values = (456, 6, logger_id, 8192, 432, commandData)
                packer = struct.Struct('>i i 16s h h 32s b')
                # Header (i = 4 byte), TransID (i = 4 byte), LoggerID (16s = 16 byte),
                # Command (h = 2 byte), Data length (h = 2 byte),	Data
                packed_data = packer.pack(*values)
            # else:
            #    values = (2, 1)
            #    packer = struct.Struct('>ih')
            #    packed_data = packer.pack(*values)

            print("5.4 Command code = %s" % command.get('commandCode'))
            print("5.5 Command data = %s" % command.get('command_data'))
            # print(int(command.get('command_data'), 0))
            log_input(ip, port, 'send ' + binascii.hexlify(packed_data))
            print("5.6 Envisoft Send command to Datalogger with command = %s" % command.get('command_data'))
            connection.sendall(packed_data)
        else:
            print("5.7 There are no commands defined in the %s" % logger_id)

        time.sleep(1)
        is_active = getDataloggerStatus(ip, logger_id)

    # values = (4, 257, 1, 100)
    # packer = struct.Struct('>ihbb')
    # packed_data = packer.pack(*values)
    # try:
    #    print("Envisoft Send command to Datalogger with packed_data = %s" % packed_data)
    #    connection.sendall(packed_data)
    # except:
    #    connection.close()
    # finally:
    #    print >> sys.stderr, 'closing socket'
    #    connection.close()
    # log_input(ip, port, "client_command_thread " + ip + ":" + port + " stop %d" % is_active)


def receive_input(connection, ip, port, max_buffer_size):
    print '----------------------------------------------------------------'
    # print("4.1.1 receive_input: Start receive data from datalogger with ip:port = %s : %s" % (ip, port))

    # Get data from data logger
    client_input = connection.recv(max_buffer_size)

    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        log_input(ip, port, "The input size is greater than expected {}".format(client_input_size))
    # decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    # result = process_input(decoded_input)

    data = client_input

    # print "4.1.1.1 Receive data from datalogger:", client_input, 'EOF'
    print '4.1.2 Received data from datalogger with data = ', repr(client_input)
    print("4.1.3 Received data from datalogger with hex data = %s" % binascii.hexlify(client_input))
    print("4.1.4 Received data len = %s" % len(data))
    log_input(ip, port, 'received ' + binascii.hexlify(data))
    log_input(ip, port, 'length %d' % len(data))

    unpacked_data = ['--QUIT--', '', 0]

    if len(data) > 0:
        # print "Received data len > 0: true"
        try:
            # unpacker = struct.Struct('>ii16shh 32s32s')
            # i = integer (4), 16s = string (16), h = integer (2)
            unpacker = struct.Struct('>ii16shh32s32s')
            unpacked_data = unpacker.unpack(data)

            log_input(ip, port, 'unpacked:  %s' % (unpacked_data,))
            print 'len(data) > 0', repr(unpacked_data)
            print 'Received datalogger value :', unpacked_data
            print 'Received datalogger value 1 = Header :', unpacked_data[0]
            print 'Received datalogger value 2 = TransID:', unpacked_data[1]
            print 'Received datalogger value 3 = LoggerID:', unpacked_data[2].decode("UTF-8").rstrip(' \t\r\n\0')
            print 'Received datalogger value 4 = Command:', unpacked_data[3]
            # print '4.1.3.2 Unpacked Value 5 = Data length:', unpacked_data[4]
            # print '4.1.3.2 Unpacked Value 6 = Data:', unpacked_data[5].decode("UTF-8").rstrip(' \t\r\n\0')
            # print '4.1.3.2 Unpacked Value 7 = Data:', unpacked_data[6]

            intCommand = int(unpacked_data[3])

            print "Command = ", intCommand

            if intCommand == 256:
                unpacked_data[0] = 'LOGIN'
                # LoggerID
                unpacked_data[1] = unpacked_data[2].decode("UTF-8").rstrip(' \t\r\n\0')
                # TransID
                unpacked_data[2] = unpacked_data[1]

            else:
                unpacked_data[0] = 'COMMAND'
                # LoggerID
                unpacked_data[1] = unpacked_data[2].decode("UTF-8").rstrip(' \t\r\n\0')
                # TransID
                unpacked_data[2] = unpacked_data[1]

            # resultLogin = login(unpacked_data[2].decode("UTF-8").rstrip(' \t\r\n\0'), "ctrluser", "1234!@#$", ip, port)
            # print '4.1.3.2 resultLogin = %s', resultLogin
            # unpacked_data = "OK"
            # if resultLogin:
            #    unpacked_data = "OK"
            #else:
            #    unpacked_data = "--QUIT--"

        except Exception as e:
            unpacked_data[0] = '--QUIT--'
            unpacked_data[1] = ''
            unpacked_data[1] = 0
            print "unpacked_data = --QUIT--"
            #print ("4.1.3.3 Failed to unpacker.unpack(data) with error: %s" + str(e))
    else:
        unpacked_data[0] = '--QUIT--'
        unpacked_data[1] = ''
        unpacked_data[1] = 0
        print 'unpacked_data = --QUIT--', repr(unpacked_data)

    result = unpacked_data
    print("Receive_input (command) form datalogger -->result = %s" % unpacked_data[0])
    print("Receive_input (decoded data) form datalogger -->result = %s" % client_input.decode("utf8").rstrip())

    return result


def login(logger_id, username, password, ip, port):
    log_input(ip, port, 'login1: ' + username + ":" + logger_id + ":" + logger_id)
    print("login: logger_id : user : pass = %s : %s" % (logger_id, username, password))
    result = False
    datalogger = db.datalogger_status.find_one({'username': username, 'password': password, 'logger_id': logger_id})
    # datalogger = db.datalogger_status.find().count()
    if datalogger:
        print("login: datalogger_status.id = %s" % (datalogger.get('_id')))
        tmp = db.datalogger_status.update_one({'_id': datalogger.get('_id')},
                                              {"$set": {'status': 1, 'ip': ip, 'port': port}})
        result = True
    else:
        result = False
    print("login: result = %s" % result)
    return result


def logout(ip, port):
    log_input(ip, port, 'logout: ' + ip + ":" + port)
    result = False
    datalogger = db.datalogger_status.find_one({'ip': ip, 'port': port}, {})
    # datalogger = db.datalogger_status.find().count()
    # print 'a %d' % datalogger
    if datalogger:
        tmp = db.datalogger_status.update_one({'_id': datalogger.get('_id')}, {"$set": {'status': 0}})
        result = True
    else:
        result = False
    return result


def getDataloggerStatus(ip, logger_id):
    result = False
    datalogger = db.datalogger_status.find_one({'ip': ip, 'logger_id': logger_id})
    if datalogger:
        if datalogger.get('status') == 1:
            result = True
        else:
            result = False
    else:
        result = False
    return result


def getDataloggerCommand(ip, logger_id):
    result = ''
    try:
        # command = db.datalogger_command.find_one({'ip': ip, 'logger_id': logger_id, 'is_process': 0})
        command = db.commands.find_one({'logger_id': logger_id, 'is_process': 0, 'status': 1})
        print("getDataloggerCommand --> logger id: %s" % logger_id)
        if command:
            print("getDataloggerCommand --> Command: %s" % command.get('title'))
            # tmp = db.datalogger_command.update_one({'_id': command.get('_id')}, {"$set": {'is_process': 1}})
            tmp = db.commands.update_one({'_id': command.get('_id')}, {"$set": {'is_process': 1}})
            print "getDataloggerCommand -->commands.update: is_process = 1"
            result = command
        else:
            result = ''
    except:
        result = ''
        print "Bind failed. Error", str(sys.exc_info())
    return result

def getDataloggerAdjustment(ip, logger_id):
    result = ''
    try:
        # command = db.datalogger_command.find_one({'ip': ip, 'logger_id': logger_id, 'is_process': 0})
        command = db.adjustments.find_one({'logger_id': logger_id, 'is_process': 0, 'status': 4})
        print("getDataloggerAdjustment --> logger id: %s" % logger_id)
        if command:
            # tmp = db.datalogger_command.update_one({'_id': command.get('_id')}, {"$set": {'is_process': 1}})
            tmp = db.adjustments.update_one({'_id': command.get('_id')}, {"$set": {'is_process': 1}})
            print "getDataloggerAdjustment --> adjustments.update_one: is_process = 1"
            result = command
        else:
            result = ''
    except:
        result = ''
        print "Bind failed. Error", str(sys.exc_info())
    return result

def process_input(input_str):
    print("Processing the input received from client")

    return "Client send " + str(input_str).upper()


def log_input(ip, port, client_input):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    if not os.path.exists(filePath):
        f = open(filePath, "a")
        f.close()

    f = open(filePath, "a")
    f.write(str(time.strftime("%H-%M-%S")) + " " + ip + ":" + port + ": " + format(client_input) + "\n")
    f.close()


if __name__ == "__main__":
    main()
