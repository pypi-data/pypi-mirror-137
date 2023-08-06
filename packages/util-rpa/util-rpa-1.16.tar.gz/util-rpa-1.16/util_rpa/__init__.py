"""A friendly Python Utilitary RPA."""

__version__ = "1.16"
__author__ = "Jonathan Bolo"

import os, re, shutil
import pysftp as sftp
import logging
from logging import NullHandler
import subprocess
import configparser
import sqlite3
from sqlite3 import Error
from datetime import datetime ,timezone
from string import ascii_lowercase
import itertools
import fnmatch

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import tarfile

from dateutil import tz
import datetime as dt
import numpy as np

LEVEL=logging.DEBUG

log=logging.getLogger(__name__)
log.addHandler(NullHandler())

def xlsx_to_csv(filename,sheet,newfilename,separator):
    import openpyxl
    import csv
    xlsx = openpyxl.load_workbook(filename)
    sheet = xlsx.active
    data = sheet.rows

    csv = open(newfilename, "w+")

    for row in data:
        l = list(row)
        for i in range(len(l)):
            
            value=''
            
            if str(l[i].value) != "None":
                value=str(l[i].value)
            
            if i == len(l) - 1:
                csv.write(value)
            else:
                csv.write(value + separator)

        csv.write('\n')

    csv.close()

    return

def upload_file_sftp(filename, destine_path, credentials):
    """ Subir archivo(s) a SFTP
    :param filename: Nombre de archivo(acepta comodines unix * ?) o lista de archivos.
    :param destine_path: Ruta destino remoto
    :param credentials: Credenciales de conexion al SFTP
    :return: None
    """
    import paramiko

    puerto = 22
    try: puerto = credentials["port"]
    except: pass

    with paramiko.Transport((credentials["hostname"], puerto)) as transport:
        # SFTP FIXES
        transport.default_window_size = paramiko.common.MAX_WINDOW_SIZE // 2
        #transport.default_max_packet_size = paramiko.common.MAX_WINDOW_SIZE
        #transport.packetizer.REKEY_BYTES   = pow(2, 40)  # 1TB max, this is a security degradation!
        #transport.packetizer.REKEY_PACKETS = pow(2, 40)  # 1TB max, this is a security degradation!
        
        # / SFTP FIXES
        transport.connect(username=credentials["username"], password=credentials["password"])
        with paramiko.SFTPClient.from_transport(transport) as server:
            server.get_channel().settimeout(100000.0)

            if type(destine_path) != str:
                raise Exception("Destino incorrecto")
            
            if str(destine_path) != "":    
                log.debug("Ubicandose en ruta remota: " + destine_path)
                server.chdir(destine_path)
            else:
                log.debug("Ubicandose en ruta default")

            if type(filename) is list:
                for p in filename:
                    log.debug ("Subiendo archivo: " + p)
                    server.put(p, destine_path + "/" + os.path.basename(p))
            else:
                
                dir_local = os.path.dirname(filename)
                if dir_local == "":
                    dir_local = "./"
                log.debug("Ubicandose en ruta local: " + dir_local)
                filename_local_comodin = os.path.basename(filename)
                dir_list = os.listdir(dir_local)
                log.debug ("Lista Local: "+ str(dir_list))

                flag_exists = False
                log.debug("Buscando coincidencias con: " + filename_local_comodin)

                for file in dir_list:

                    if fnmatch.fnmatch(file, filename_local_comodin):
                        flag_exists = True
                        filename_local = os.path.join(dir_local, file)
                        log.debug ("Subiendo archivo: " + filename_local)
                        server.put(filename_local, destine_path + "/" + file)
                
                if not flag_exists:
                    raise Exception("No se encontró coincidencias para: " + filename)
    
    return

def makedir_sftp(sftp_path, credentials, recursive = False):
    """ Crea directorio SFTP
    :param sftp_path: Directorio remoto a crear
    :param credentials: Credenciales de conexion al SFTP
    :return: None
    """
    import paramiko

    puerto = 22
    try: puerto = credentials["port"]
    except: pass
    
    with paramiko.Transport((credentials["hostname"], puerto)) as transport:
        # SFTP FIXES
        transport.connect(username=credentials["username"], password=credentials["password"])
        with paramiko.SFTPClient.from_transport(transport) as server:
            server.get_channel().settimeout(100000.0)

            log.info("Inicio creacion directorio:" + sftp_path)

            if recursive:

                folder_list = str(sftp_path).split("/")

                print(folder_list)

                ini = 0
                ini_dir = ""

                if sftp_path[0:1] == "/":
                    log.info("Trabajando con directorio absoluto '/' ")
                    ini = 1
                    ini_dir = "/"

                for i in range(ini + 1 , len(folder_list) + 1):

                    abs_path = ini_dir + "/".join(folder_list[ini:i])
                    exists = False
                    try:
                        server.stat(abs_path)
                        exists = True
                    except:
                        pass

                    if not exists:
                        log.info("Creando directorio recursivo:" + abs_path)
                        server.mkdir(abs_path, mode=755)
                    else:
                        log.info("Directorio recursivo ya existe:" + abs_path)
                        continue

            else:
                exists = False
                try:
                    server.stat(sftp_path)
                    exists = True
                except:
                    pass

                if not exists:
                    log.info("Creando directorio no recursivo:" + sftp_path)
                    server.mkdir(sftp_path, mode=755)
                else:
                    log.info("Directorio no recursivo ya existe:" + sftp_path)

def list_sftp(sftp_path, credentials, attr=False):
    """ Lista archivo(s) de un directorio SFTP
    :param sftp_path: Directorio remoto a listar
    :param credentials: Credenciales de conexion al SFTP
    :param attr: Flag que activa el retorno de (list of SFTPAttributes) en vez de los clasicos (list of str)
    :return: None
    """
    import paramiko

    puerto = 22
    try: puerto = credentials["port"]
    except: pass

    with paramiko.Transport((credentials["hostname"], puerto)) as transport:
        # SFTP FIXES
        transport.default_window_size = paramiko.common.MAX_WINDOW_SIZE // 2
        #transport.default_max_packet_size = paramiko.common.MAX_WINDOW_SIZE
        #transport.packetizer.REKEY_BYTES   = pow(2, 40)  # 1TB max, this is a security degradation!
        #transport.packetizer.REKEY_PACKETS = pow(2, 40)  # 1TB max, this is a security degradation!
        
        # / SFTP FIXES
        transport.connect(username=credentials["username"], password=credentials["password"])
        with paramiko.SFTPClient.from_transport(transport) as server:
            server.get_channel().settimeout(100000.0)

            server.chdir(sftp_path)
            if attr:
                filelist = server.listdir_attr()
            else :
                filelist = server.listdir()
            return filelist

def remove_sftp(list_files_sftp, credentials, attr=False):
    """ Borra archivo(s) del sftp
    :param list_files_sftp: Lista de archivos a borrar
    :param credentials: Credenciales de conexion al SFTP
    :return: None
    """
    import paramiko

    puerto = 22
    try: puerto = credentials["port"]
    except: pass

    with paramiko.Transport((credentials["hostname"], puerto)) as transport:
        # SFTP FIXES
        transport.default_window_size = paramiko.common.MAX_WINDOW_SIZE // 2
        #transport.default_max_packet_size = paramiko.common.MAX_WINDOW_SIZE
        #transport.packetizer.REKEY_BYTES   = pow(2, 40)  # 1TB max, this is a security degradation!
        #transport.packetizer.REKEY_PACKETS = pow(2, 40)  # 1TB max, this is a security degradation!
        
        # / SFTP FIXES
        transport.connect(username=credentials["username"], password=credentials["password"])
        with paramiko.SFTPClient.from_transport(transport) as server:
            server.get_channel().settimeout(100000.0)
            
            for file in list_files_sftp:
                try:
                    log.info("Borrando archivo: " + file)
                    server.remove(file)
                except Exception as e:
                    log.info(str(e))
                    log.info("Ocurrio un error al borrar el archivo: " + file)
    
def download_file_sftp(filename, destine_path, credentials, flag_remove = False):
    """ Descargar archivo(s) SFTP
    :param filename: Nombre de archivo(acepta comodines unix * ?) o lista de archivos.
    :param destine_path: Ruta destino remoto
    :param credentials: Credenciales de conexion al SFTP
    :param flag_remove: Flag que determina borrar o no los archivos remotos una vez descargados
    :return: None
    """

    import paramiko
    
    if not os.path.exists(destine_path):
        raise Exception("Directorio destino no existe: " + destine_path)
    
    puerto = 22
    try: puerto = credentials["port"]
    except: pass
    
    with paramiko.Transport((credentials["hostname"], puerto)) as transport:
        # SFTP FIXES
        transport.default_window_size = paramiko.common.MAX_WINDOW_SIZE // 2
        #transport.default_max_packet_size = paramiko.common.MAX_WINDOW_SIZE
        #transport.packetizer.REKEY_BYTES   = pow(2, 40)  # 1TB max, this is a security degradation!
        #transport.packetizer.REKEY_PACKETS = pow(2, 40)  # 1TB max, this is a security degradation!
        
        # / SFTP FIXES
        transport.connect(username=credentials["username"], password=credentials["password"])
        with paramiko.SFTPClient.from_transport(transport) as server:
            #server.get_channel().settimeout(100000.0)

            if type(filename) is list:
                for file in filename:
                    
                    dir_remoto = os.path.dirname(file)
                    filename_remoto = os.path.basename(file)
                    log.debug("Ubicandose en ruta: " + dir_remoto)
                    server.chdir(dir_remoto)
                    
                    destine = os.path.join(destine_path, filename_remoto)
                    log.debug("Obteniendo archivo: " + file)
                    log.debug ("Ruta Destino: " + destine)
                    
                    server.get( file, destine )
                    
                    if flag_remove:
                        server.remove(file)
            else:

                dir_remoto = os.path.dirname(filename)
                filename_remoto_comodin = os.path.basename(filename)
                log.debug("Ubicandose en ruta: " + dir_remoto)

                server.chdir(dir_remoto)
                dir_list = server.listdir()
                log.debug ("Lista SFTP: "+ str(dir_list))
            
                
                log.debug("Buscando coincidencias con: " + filename_remoto_comodin)

                for file in dir_list:
                    
                    if fnmatch.fnmatch(file, filename_remoto_comodin):
                        flag_exists = True
                        filename_remoto = os.path.join(dir_remoto, file)
                        log.debug ("Obteniendo archivo: " + filename_remoto)

                        log.debug ("Ruta Destino: " + destine_path)
                        destine = os.path.join(destine_path, file)
                        server.get( file, destine )
                        
                        if flag_remove:
                            server.remove(filename)
                            
                if not flag_exists:
                    raise Exception("No se encontró coincidencias para: " + filename)
    
def download_by_prefix_sftp(sftpPath, prefix, downloadPath, credentials, flag_remove = False):    
    import paramiko

    puerto = 22
    try: puerto = credentials["port"]
    except: pass

    with paramiko.Transport((credentials["hostname"], puerto)) as transport:
        # SFTP FIXES
        transport.default_window_size = paramiko.common.MAX_WINDOW_SIZE // 2
        #transport.default_max_packet_size = paramiko.common.MAX_WINDOW_SIZE
        #transport.packetizer.REKEY_BYTES   = pow(2, 40)  # 1TB max, this is a security degradation!
        #transport.packetizer.REKEY_PACKETS = pow(2, 40)  # 1TB max, this is a security degradation!
        
        # / SFTP FIXES
        transport.connect(username=credentials["username"], password=credentials["password"])
        with paramiko.SFTPClient.from_transport(transport) as server:
            server.get_channel().settimeout(100000.0)

            server.chdir(sftpPath)
            filelist = server.listdir()
            log.debug ("Lista SFTP: "+ str(len(filelist)))
            #print(filelist)
            for filename in filelist:
                path_file=os.path.join(downloadPath, filename)
                exists = prefix in filename
                if exists:
                    log.debug ("Obteniendo archivo: " + sftpPath + filename)
                    log.debug ("Ruta Destino: " + downloadPath + filename)
                    server.get(filename,path_file)

                    if flag_remove:
                        if os.path.exists(path_file ):
                            server.remove(filename)
                        else:
                            logging.error ("Ocurrio un error al obtener el archivo: " + path_file)
                            continue
    
    return

def move_sftp(filenames, credentials):
    """ Renombra un archivo en SFTP
    :param filenames: Dictionario tipo 'Archivo original':'Archivo renombrado' (rutas absolutas)
    :param credentials: Credenciales de conexion al SFTP
    :return: None
    """
    import paramiko

    puerto = 22
    try: puerto = credentials["port"]
    except: pass
    
    with paramiko.Transport((credentials["hostname"], puerto)) as transport:
        # SFTP FIXES
        transport.default_window_size = paramiko.common.MAX_WINDOW_SIZE // 2
        #transport.default_max_packet_size = paramiko.common.MAX_WINDOW_SIZE
        #transport.packetizer.REKEY_BYTES   = pow(2, 40)  # 1TB max, this is a security degradation!
        #transport.packetizer.REKEY_PACKETS = pow(2, 40)  # 1TB max, this is a security degradation!
        
        # / SFTP FIXES
        transport.connect(username=credentials["username"], password=credentials["password"])
        with paramiko.SFTPClient.from_transport(transport) as server:
            server.get_channel().settimeout(100000.0)

            if not type(filenames) is dict:
                raise Exception("Filename is not dict")
            
            for origin, destine in filenames.items():
                log.debug("Moviendo: " + origin + " hacia " + destine)
                server.rename(origin,destine)

def get_info_pdf(file):
    import fitz
    doc = fitz.open(file)
    page_count = doc.pageCount
    p = doc.loadPage(0)       
    return p.getText()

def send_mail_by_exe(credentials, mail):
    path = os.path.dirname(__file__)
    program = os.path.join(path,'mail.exe')
    
    try:
        arguments =   credentials['username'] + '|' + credentials['password'] + '|'
        arguments +=  credentials['server']   + '|' + credentials['port']     + '|'
        arguments +=  mail['sender'] + '|' + mail['reciepients'] + '|' + mail['cc']         +'|' 
        arguments +=  mail['body']   + '|' + mail['subject']     + '|' + mail['attachment'] 
    except IndexError as e:
        log.error("Uno de los campos email no fue encontrado")
        raise Exception(e)
    
    try:
        subprocess.call([program, arguments])
    except Exception as e:
        log.error("Ocurrio un error al ejecutar:" + program)
        raise Exception(e)

def create_folders(lista_carpetas):
    '''
    Funcion que crea carpetas de trabajo
    '''
    for carpeta in lista_carpetas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
def create_folder_env(dir_path):
    '''
    Funcion que crea las carpetas de trabajo estándar de trabajo
    '''
    dir_in = os.path.join(dir_path,"input")
    dir_out = os.path.join(dir_path,"output")
    dir_log = os.path.join(dir_path,"log")
    
    if not os.path.exists(os.path.join(dir_in,"backup")):
        os.makedirs( os.path.join(dir_in,"backup") )
    
    if not os.path.exists(os.path.join(dir_out,"backup")):
        os.makedirs( os.path.join(dir_out,"backup") )

    if not os.path.exists(dir_log):
        os.makedirs( dir_log )
    
    return

def config_logging(file_log="", level=logging.DEBUG, console=True):
    '''
    Funcion que configura la gestion de Logs
    '''
    
    formatter = logging.Formatter('%(asctime)-5s %(filename)s %(lineno)d %(levelname)-8s %(message)s')
    
    #logging file
    if file_log != "":
        fh = logging.FileHandler(file_log)
        fh.setLevel(level=level)
        fh.setFormatter(formatter)
    if console:
        ch = logging.StreamHandler()
        ch.setLevel(level=level)
        ch.setFormatter(formatter)
    
    log=logging.getLogger(__name__)
    
    if file_log:
        log.addHandler(fh)
    
    if console:
        log.addHandler(ch)
    
    log.info("Level log: " + logging.getLevelName(level))
    
    return log

def check_if_string_in_file(filename, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(filename, 'r', errors='ignore', encoding='utf-8') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search.lower() in line.lower():
                return True
    return False

class Configuration(object):
    """
    Clase que permite cargar dinámicamente los archivos de configuración del proceso.
    """
    
    def __init__(self, file_config="Config.ini", section_names=["DEFAULT"]):
        r"""Inicializa los parametros de entrada
        :param file_config: Ruta absoluta del archivo de configuración.
        :param section_names: (optional) Lista de secciones a cargar.
        :return: :class: object
        """
        parser = configparser.ConfigParser(interpolation=EnvInterpolation())
        parser.optionxform = str
        found = parser.read(file_config)

        if not found:
            raise ValueError('Archivo de configuracion no encontrado.')
        
        self.parser = parser

        # Cargando configuracion
        for name in section_names:
            self.__dict__.update(parser.items(name))
    
class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)

def create_connection_sqlite(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def get_now_format(format = "%Y%m%d%H%M%S%f"):
    return str(datetime.now().strftime(format))

def replace_string_in_file(filename_in, filename_out, dict_words):
    """ Reemplaza cadenas de un archivo
    :param filename_in: Archivo de entrada
    :param filename_out: Archivo de salida
    :param dict_words: Diccionario de palabras y valores a reemplazar
    :return: None
    """

    write_obj = open(filename_out, 'w')

    line = ""

    with open(filename_in, 'r') as read_obj:
        for line in read_obj:

            for k, v in dict_words.items():
                line = line.replace(k, v)

            #log.debug(line)
            write_obj.write(line)

    write_obj.close()

def sqlcmd(file_sql, credentials, file_sql_log, dict_variable = {}, validate_error = True, coding = "65001"):
    """ Ejecuta el utilitario SQLCMD de SQLServer en linea de comandos
    :param file_sql: Archivo sql a ejecutar
    :param credentials: Credenciales de conexion a la Base de Datos SQLServer
    :param file_sql_log: Archivo prefijo para generar archivo log (file_sql_log + ".ahora.db")
    :param dict_variable: Diccionario de palabras y valores a reemplazar en el script sql
    :param validate_error: Flag para generar exception si se encuentra la palabra error
    :param coding: Formato de codificacion
    :return: None
    """

    if os.name == 'nt':
        sqlcmd_bin = 'sqlcmd'
    else:
        sqlcmd_bin= '/opt/mssql-tools/bin/sqlcmd'
    
    if not os.path.exists(file_sql):
        raise FileNotFoundError(file_sql)

    if file_sql_log == "":
        raise Exception("Se necesita ingresar archivo log")
    
    file_sql_tmp = file_sql + ".tmp"

    if len(dict_variable) > 0:
        if os.path.exists(file_sql_tmp):
            os.remove(file_sql_tmp)
        replace_string_in_file( file_sql, file_sql_tmp, dict_variable)
    else:
        shutil.copy(file_sql, file_sql_tmp)
    
    
    cmd = (sqlcmd_bin + ' -e -y 0'  + 
                        ' -i ' + file_sql_tmp            +
                        ' -o ' + file_sql_log            +
                        ' -S ' + credentials['hostname'] +
                        ' -d ' + credentials['database'] + 
                        ' -U ' + credentials['username'] +
                        ' -P ' + credentials['password'] +
                        ' -f ' + coding )
    
    log.debug("Ejecutando sql")
    log.debug(cmd)
        
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    while proc.poll() is None:
        line = proc.stdout.readline()
        #log.debug(line.rstrip())
        if isinstance(line, bytes):
            str_line = line.decode("utf-8")
        else:
            str_line = line
        
        if str_line != "":
            log.debug(str_line)
    
    os.remove(file_sql_tmp)

    if os.path.exists(file_sql_log):
        log.debug( open(file_sql_log, "r", encoding='utf-8', errors='ignore').read() )
    
        if validate_error:
            if check_if_string_in_file(file_sql_log, "error"):
                raise Exception("Se encontro un error en el archivo log de la BD.")
    else:
        raise Exception("Archivo output sqlcmd no generado.")

def bcp(table, file, operation, credentials, file_sql_log, validate_error = True, coding = "-C 65001"):
    """ Ejecuta el utilitario SQLCMD de SQLServer en linea de comandos
    :param table: Tabla a trabajar
    :param file: Archivo de entrada o salida segun la operacion
    :param operation: operacion a ejecutar IN u OUT
    :param credentials: Credenciales de conexion a la Base de Datos SQLServer
    :param file_sql_log: Archivo prefijo para generar archivo log (file_sql_log + ".ahora.db")
    :param validate_error: Flag para generar exception si se encuentra la palabra error
    :param coding: Formato de codificacion
    :return: None
    """
    
    if os.name == 'nt':
        bcpcmd_bin = 'bcp'
    else:
        bcpcmd_bin= '/opt/mssql-tools/bin/bcp'
    
    if file_sql_log == "":
        raise Exception("Se necesita ingresar archivo log")
    
    if not operation in ("IN","OUT"):
        raise Exception("Operacion BCP no permitida")

    cmd = (bcpcmd_bin + ' ' + table + ' ' + operation + ' "' + file + '"' + 
                ' -e ' + file_sql_log            +
                ' -S ' + credentials['hostname'] +
                ' -d ' + credentials['database'] + 
                ' -U ' + credentials['username'] +
                ' -P ' + credentials['password'] +
                ' -c ' + coding +
                ' -b1000 -m1000 -t"|"' )
    
    log.debug("Ejecutando sql")
    log.debug(cmd)
        
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    while proc.poll() is None:
        line = proc.stdout.readline()
        #log.debug(line.rstrip())
        if isinstance(line, bytes):
            str_line = line.decode("utf-8")
        else:
            str_line = line
        
        if str_line != "":
            log.debug(str_line)

    if os.path.exists(file_sql_log):
        log.debug( open(file_sql_log, "r", encoding='utf-8').read() )
    
        if validate_error:
            if check_if_string_in_file(file_sql_log, "error"):
                raise Exception("Se encontro un error en el archivo log de la BD.")
    else:
        raise Exception("Archivo output bcp no generado.")

def get_data_from_sqllog(file_sql_log, file_result, prefix = "DATA:"):
    """ Filtra las lineas de texto que comiencen con el prefijo
    :param file_sql_log: Archivo de entrada a analizar
    :param file_result: Archivo de salida con data filtrada
    :param prefix: Prefijo a analizar
    :return: None
    """
    if not os.path.exists(file_sql_log):
        raise FileNotFoundError(file_sql_log)
    
    file_out = open(file_result, "w", encoding='utf-8')

    with open(file_sql_log, 'r', encoding='utf-8', errors='ignore') as res:
        f_data = False

        for line in res:
            if re.match("INI_DATA_SQLSERVER", line):
                log.debug("UBICADO:"+line)
                f_data = True
            if f_data and re.search(prefix, line):
                file_out.write(line.replace(prefix,""))

    file_out.close()

def iter_all_strings():
    """ Generator que devuelve lista de letras secuenciales
    :return: yield
    """
    for size in itertools.count(1):
        for s in itertools.product(ascii_lowercase, repeat=size):
            yield "".join(s)

def enviar_correo_smtp(mail):
    """ Funcion que envia correos via SMTP
    :return: bool
    """
    try:
        email_smtp_host  = mail['smtp_host']
        email_smtp_port  = mail['smtp_port']
        email_from       = mail['from']
        email_to         = mail['to'].split(';')
        email_cc         = mail['cc'].split(';')
        email_subject    = mail['subject']
        email_body       = mail['body']
        email_attachment = mail['attachment']
    except Exception as e:
        log.info(e, exc_info=True)
        log.info("Uno de los parametros del correo no esta definido")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = ','.join(email_to)
        msg['Subject'] = email_subject
        msg['cc'] = ','.join(email_cc)

        msg.attach(MIMEText(email_body, 'html', 'utf-8'))
        #msg.attach(MIMEText(email_body,'plain'))

        emails = email_to + email_cc

        filename = mail['attachment']

        if filename != "":
            for filename in email_attachment.split(";"):
                attachment = open(filename,'rb')
                part = MIMEBase('application','octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',"attachment; filename= "+ os.path.basename(filename))
                msg.attach(part)

        text = msg.as_string()
        server = smtplib.SMTP(host=email_smtp_host, port=email_smtp_port)

        server.sendmail(email_from, emails, text)
        server.quit()
    except Exception as e:
        log.info(e, exc_info=True)
        log.info("Ocurrio un error al enviar el correo")
        return False

    return True

def comprimir(lista_objetos = [], nombre_salida = "archivo_salida", tipo_compresion = "tgz"):
    """ Funcion que comprime archivos y carpetas
    :return: None
    """
    if tipo_compresion == "tgz":
        try:
            with tarfile.open( nombre_salida + ".tgz", "w:gz" ) as tar:
                for name in lista_objetos:
                    tar.add(name)
                tar.list()
        except Exception as e:
            log.error(str(e),exc_info=True)
            raise Exception("Ocurrio un error en la compresion")
    else:
        raise Exception("Tipo compresion no identificada")

def convertir_local_a_utc(fecha_local):
    fecha_local = fecha_local.replace(tzinfo=tz.tzlocal())
    fecha_utc = fecha_local.astimezone(tz.tzutc())
    return fecha_utc

class RpaNotificacionCorreo:
    """
    Clase que define la configuracion y metodos para el envio de Correo.
    """
    def __init__(self, host="10.226.5.191", port="25", secure_mode=None, use_executable=False, **kwargs):
        """
        Funcion que carga los valores plantilla del correo a enviar.
        
        Parameters
        ----------
        host : str
            Ip del servidor de correos SMTP.
        port : str
            Puerto del servidor de correos SMTP.
        secure_mode : str. Opcional
            Modo seguro para autenticarse. Solo puede ingresarse SSL o TLS.
        use_executable : bool. Opcional
            Booleano que determina si se debe o no usar el .exe (contigencia).
            
        **kwargs : optional
            Parametros opcionales para la autenticacion
            user
            password

        Returns
        -------
        None
            
        Raises
        ------
        ValueError
            Si existe alguna inconsistencia en los parametros de entrada
        """
        self.host = host
        self.port = port
        
        # Definiendo modo seguro
        self.secure_mode = None
        if secure_mode:
            if not isinstance(secure_mode, str) or secure_mode not in ["SSL","TLS"] :
                raise ValueError("secure_mode: Solo pude ingresar el modo seguro SSL o TLS")
            self.secure_mode = secure_mode
        
        # Definiendo autenticacion. Por defecto se usa relay smtp.
        self.use_auth = False
        if 'user' in kwargs and 'password' in kwargs:
            self.use_auth = True
            self.user = kwargs['user']
            self.password = kwargs['password']
        
        # Definiendo uso de contingenca .exe (Cuando no existe relay y los metodos SMTP
        # desarrollados hasta ahora no soportan el envio)
        self.use_executable = use_executable
        
        self.subject    = ''
        self.body       = ''
        self.email_from = ''
        self.email_to   = []
        self.email_cc   = []
        self.email_cco  = []

    def __str__(self):
        """
        Funcion que devuelve los parametros configurados en los atributos.
        
        Returns
        -------
        String
            Servidor + Plantilla
        """
        con = ''
        if not self.use_auth:
            con += "Servidor : " + self.host + ":" + self.port + "\n"
        else:
            con += "Servidor: " + self.user + "/" + self.password + "@" + self.host + ":" + self.port + "\n"

        con += "Plantilla From   : " + self.email_from + "\n"
        con += "Plantilla To     : " + str(self.email_to ) + "\n"
        con += "Plantilla Cc     : " + str(self.email_cc ) + "\n"
        con += "Plantilla Cco    : " + str(self.email_cco) + "\n"
        con += "Plantilla Subject: " + self.subject + "\n"
        con += "Plantilla Body   : " + self.body
        
        return con        
    
    def cargar_plantilla(self, subject_template=None, body_template=None, email_from=None, email_to=None, email_cc=None, email_cco=None):
        """
        Funcion que carga los valores plantilla del correo a enviar.
        
        Parameters
        ----------
        subject_template : str. Opcional
            Asunto plantilla a usar en el correo.
        body_template : str. Opcional
            Cuerpo plantilla a usar en el correo.
        email_from : str
            Emisor a colocar en el correo a enviar. 
        email_to : str. Opcional
            Destinatarios a colocar en el correo a enviar. Si existe mas de uno,
            colocar como separador ';'
        email_cc : str. Opcional
            Destinatarios Con Copia a colocar en el correo a enviar. Si existe mas de uno,
            colocar como separador ';'
        email_cco : str. Opcional
            Destinatarios Con Copia Oculta a colocar en el correo a enviar. Si existe mas de uno,
            colocar como separador ';'
        
        Returns
        -------
        None
            
        Raises
        ------
        ValueError
            Si existe alguna inconsistencia en los parametros de entrada
        """
        
        if subject_template:
            self.subject = subject_template
        
        if body_template:
            self.body = body_template
        
        if type(email_from) not in [str]:
            raise ValueError("From: Debe ingresar un correo")
        
        if type(email_to) not in [str, type(None)]:
            raise ValueError("From: Debe ingresar una cadena de correo(s) separados por ';'")
        
        if type(email_cc) not in [str, type(None)]:
            raise ValueError("Cc: Solo puede ingresar una cadena de correos separado por ';'")
        
        if type(email_cco) not in [str, type(None)]:
            raise ValueError("Cco: Solo puede ingresar una cadena de correos separado por ';'")
        
        if type(email_to) == None and type(email_cc) == None and type(email_cco) == None:
            raise ValueError("Debe ingresar al menos un correo destinatario")
        
        self.email_from = email_from
        self.email_to   = email_to.split(";")  if type(email_to)  == str else []
        self.email_cc   = email_cc.split(";")  if type(email_cc)  == str else []
        self.email_cco  = email_cco.split(";") if type(email_cco) == str else []
        
    def enviar_correo(self, subject_replace=None, body_replace=None, attachment_files=None):
        """
        Funcion que envia correos.
        
        Parameters
        ----------
        subject_replace : dict. Opcional
            Palabras clave a reemplazar en el asunto del correo. Cada llave del diccionario 
            será buscada en la plantilla cargada inicialmente y reemplazada por su valor.
        body_replace : dict. Opcional
            Palabras clave a reemplazar en el cuerpo del correo. Cada llave del diccionario 
            será buscada en la plantilla cargada inicialmente y reemplazada por su valor.
        attachment_files : str. Opcional
            Cadena de archivos a adjuntar en el correo. Los archivos deben tener la ruta
            absoluta y estar separados por ';' en caso de existir mas de uno.
        
        Returns
        -------
        Boolean
            Se devolvera True si es que no se genero alguna excepcion. De lo contrario el valor
            devuelto sera False.
        
        Raises
        ------
        Exception
            Si existe una excepcion en el flujo, solo se captura e imprime el exc_info.
        """
        
        try:
            # Armando subject
            subject = self.subject
            if subject_replace:
                if type(subject_replace) != dict:
                    raise ValueError("Subject Replace: Debe ingresar un diccionario con las palabras clave a reemplazar")  
                for i in subject_replace:
                    subject = str(subject).replace(i, subject_replace[i])
            
            # Armando body
            body = self.body
            if body_replace:
                if type(body_replace) != dict:
                    raise ValueError("Body Replace: Debe ingresar un diccionario con las palabras clave a reemplazar")
                for i in body_replace:
                    body = body.replace(i, body_replace[i])
            
        except Exception as e:
            log.info(e, exc_info=True)
            log.info("Ocurrio un error al enviar el correo")
            return False

        if not self.use_executable:
            log.info("Envio de correo via SMTPLib")
            try:
                msg = MIMEMultipart()
                msg['From'] = self.email_from
                msg['To']   = ','.join(self.email_to)
                msg['cc']   = ','.join(self.email_cc)
                msg['cco']  = ','.join(self.email_cco)
                msg['Subject'] = subject
                
                # Integrando
                msg.attach(MIMEText(body, 'html', 'utf-8'))
                
                # Armando lista de correos
                emails = self.email_to + self.email_cc + self.email_cco

                # Ingresando adjunto
                if attachment_files:
                    for filename in attachment_files.split(";"):
                        attachment = open(filename,'rb')
                        part = MIMEBase('application','octet-stream')
                        part.set_payload((attachment).read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition',"attachment; filename= "+ os.path.basename(filename))
                        msg.attach(part)

                # Enviando
                text = msg.as_string()
                
                if not self.secure_mode:
                    # Usado en el relay smtp telefonica robotizacion
                    server = smtplib.SMTP(host=self.host, port=self.port)
                    if self.use_auth:
                        # Habilitado si es que en algun momento se necesita autenticar
                        server.login(self.user, self.password)
                else:
                    # Habilitado para conexiones seguras en el futuro
                    if self.secure_mode == "SSL":
                        server = smtplib.SMTP_SSL(host=self.host, port=self.port)
                    if self.secure_mode == "TLS":
                        server = smtplib.SMTP(host=self.host, port=self.port)
                        server.starttls()
                    
                    if self.use_auth:
                        server.login(self.user, self.password)           
                
                server.sendmail(self.email_from, emails, text)
                server.quit()
            except Exception as e:
                log.info(e, exc_info=True)
                log.info("Ocurrio un error al enviar el correo")
                return False
        else:
            log.info("Envio de correo via executable")
            try:
                path = os.path.dirname(__file__)
                program = os.path.join(path, 'bin', 'mail.exe')

                attachment = ''
                if attachment_files:
                    attachment = attachment_files                

                arguments =   self.user + '|' + self.password + '|'
                arguments +=  self.host + '|' + self.port     + '|'
                arguments +=  self.email_from + '|' + ";".join(self.email_to) + '|' + ";".join(self.email_cc) + '|' 
                arguments +=  body + '|' + subject + '|' + attachment
            except IndexError as e:
                log.info(e, exc_info=True)
                log.error("Uno de los campos email no fue encontrado")
                return False
            
            try:
                subprocess.call([program, arguments])
            except Exception as e:
                log.error("Ocurrio un error al ejecutar:" + program)
                return False
            
        return True

#Función del bisiesto en el util.rpa
def isleap(year):
    """Return True for leap years, False for non-leap years."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def feriados_santos(anio):
    """Función de feriados santos"""
    #Calcular el resto de la division año/19
    a = anio%19
    #Calcular el cociente entero de la division año/100
    b = anio//100
    #Calcular el resto de la division año/100
    c = anio%100
    #Calcular cociente de la división b/4
    d = b//4
    #Calcular el resto de la división b/4
    e = b%4
    #Calcular el cociente de la división (b+8)/25
    f = (b+8)//25
    #Calcular el cociente de la división (b-f+1)/3
    g = (b-f+1)//3
    #Calcular el resto de la división (19*a+b-d-g+15)/30
    h = (19*a+b-d-g+15)%30
    #Calcular el cociente de la división c/4
    i = c//4
    #Calcular el resto de la división c/4
    k = c%4
    #Calcular el resto de la división (32+2*e+2*i-h-k)/7
    l = (32+2*e+2*i-h-k)%7
    #Calcular el cociente de la división (a+11*h+22*l)/451
    m = (a+11*h+22*l)//451
    #Calcular la suma h+l-7*m+114
    n = h+l-7*m+114
    #Mes,Calcular el cociente de la división n/31
    mes = n//31
    #Dia,calcular 1 + (el resto de n/31) o bien 1+(n-(mes*31))
    dia = 1+n%31

    pascua = datetime(anio,mes,dia)
    jueves_santo = pascua - dt.timedelta(3)
    viernes_santo = pascua - dt.timedelta(2)
    dia_jueves = jueves_santo.timetuple().tm_yday
    dia_viernes = viernes_santo.timetuple().tm_yday
    return (dia_jueves,dia_viernes)

def lista_feriados(anio):
    """Función que añade los feriados de semana santa a los feriados predefinidos"""
    #Lista de feriados fijos 
    lista_feriados  =  np.array([1,121,180,209,210,242,281,305,342,343,359], dtype=int)
    #Añadir feriados de semana santa
    jueves,viernes = feriados_santos(anio)
    lista_feriados = np.append(lista_feriados,[jueves,viernes],axis = 0)
    lista_feriados.sort()
    #Si es bisiesto sumar 1 a los días después de Febrero 29 (día 60)
    if isleap(anio):
        log.info("El año " + str(anio) + " es un año bisiesto")
        feriados_afectados = np.fromiter((element + 1 for element in lista_feriados if element > 60), dtype = lista_feriados.dtype)
        feriados_desafectados = np.fromiter((element for element in lista_feriados if element <= 60), dtype = lista_feriados.dtype)
        lista_feriados = np.concatenate((feriados_desafectados,feriados_afectados),axis=0)
    
    return list(lista_feriados)