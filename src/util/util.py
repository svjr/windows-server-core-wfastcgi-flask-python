import os
from datetime import datetime

from werkzeug.utils import secure_filename

from src.common.app_common import path_app_data_unsuccessful
from src.config.log_config import logger

allowed_extensions = {'csv', 'CSV'}


def print_header():
    logger.info("*****************************************************")
    logger.info("************** INICIANDO PROCESSAMENTO **************")
    logger.info("*****************************************************")
    logger.info('')


def print_footer():
    logger.info('')
    logger.info('')
    logger.info("*****************************************************")
    logger.info("************** TERMINO DO PROCESSAMENTO *************")
    logger.info("*****************************************************")
    logger.info('')
    logger.info('')


def move_file_datetime(path_aquivo, formato_data, formato_hora, path_destino):
    logger.info("")
    logger.info("Inicio do Metodo [mover_arquivo_com_data_hora]")
    logger.info("Movendo arquivo [" + path_aquivo + "] para pasta [" + path_destino + "] ...")
    data_atual = datetime.now()
    data_file_discard = data_atual.strftime(formato_data) + "_" + data_atual.strftime(formato_hora + "_")
    ultima_posicao_barra = path_aquivo.rfind("/")
    novo_nome_arquivo = path_destino + "/" + data_file_discard + path_aquivo[ultima_posicao_barra + 1:]
    logger.info("Novo nome do arquivo [" + novo_nome_arquivo + "]")
    os.rename(path_aquivo, novo_nome_arquivo)


def is_extension_csv(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_list_files_csv_in_folder(path_folder, order_desc=True):
    files = os.listdir(path_folder)
    files = list(filter(lambda f: f.endswith('.csv'), files))
    files = [path_folder + "/" + f for f in files]
    return sorted(files, key=lambda p: os.stat(p).st_mtime, reverse=order_desc)


def rename_columns_dataframe(strSearch, strNew, df):
    logger.info('Inicio do metodo [__rename_columns_dp_csv]')
    df.columns = df.columns.str.replace(strSearch, strNew)
    df.columns = df.columns.str.lower()
    logger.info("Termino do metodo [__rename_columns_dp_csv]")
    return df


def save_file_csv_from_request(request,
                               field_request,
                               path_folder,
                               discard_files_existing=True):
    logger.info("Inicio do método [salvar_arquivo_csv_from_request]")
    file = request.files[field_request]

    if field_request not in request.files:
        raise Exception("O campo [" + field_request + "] NÃO está presente na requisição.....")
    if file.filename == '' or file.filename is None:
        raise Exception("Nenhum arquivo foi enviado na requisição...")
    if file and not is_extension_csv(file.filename):
        raise Exception("Extensão do arquivo enviado é inválida. Extensões permitidas" + str(allowed_extensions))

    if discard_files_existing:
        logger.info("Movendo arquivos anteriores para a pasta de descartados...")
        files_in_path = os.listdir(path_folder)
        files_in_path = list(filter(lambda f: f.endswith('.csv'), files_in_path))
        files_in_path = [path_folder + "/" + f for f in files_in_path]
        for index, filename in enumerate(files_in_path):
            move_file_datetime(path_aquivo=files_in_path[index],
                               formato_hora='%Y%m%d',
                               formato_data='%H%M%S',
                               path_destino=path_app_data_unsuccessful)

    filename = secure_filename(file.filename)
    filename_path = path_folder + "/" + filename
    file.save(filename_path)
    file_name = file.filename.rsplit('.', 1)[0]
    file_type = file.filename.rsplit('.', 1)[1]
    logger.info("    Nome Arquivo: [" + file_name + "]")
    logger.info("Extensão Arquivo: [" + file_type + "]")
    return filename_path
