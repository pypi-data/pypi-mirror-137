import os
import math, hashlib, requests, json, getopt, sys
import tempfile
base_url = "http://202.109.131.111:8012/"


def file_chunk_spilt(path, chunk_size, pi, session):
    """
    文件按照数据块大小分割为多个子文件
    INPUT -> 文件目录, 文件名, 每个数据块大小
    """
    total_size = os.path.getsize(path)
    # 计算文件的总片数
    total_chunks = math.ceil(total_size / chunk_size)
    # 计算文件的md5
    identifier = get_file_md5(path)
    # 获取文件的file_name
    file_name = path.split("/")[-1]
    # file_name = path.split("\\")[-1]
    # 发送第一次get请求， 判断是否已经上传和已上传的分片id
    res = upload_get(identifier, pi, file_name, total_size, total_chunks, session)
    # 判断是否成功
    if res and res.status_code == 200:
        res_data = json.loads(res._content)
        if int(res_data["ret_code"]) == 1:
            return "上传成功"
        else:
            upload_id = res_data["ret_data"]["upload_id"]
            file_id = res_data["ret_data"]["uuid"]
            uploaded_chunks = res_data["ret_data"]["uploaded_chunks"]
    else:
        return "上传失败"

    if total_size > chunk_size:
        chunk_number = 0
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                chunk_number += 1
                current_chunk_size = len(chunk)
                if chunk_number in uploaded_chunks:
                    continue
                fd, name = tempfile.mkstemp()
                try:
                    with os.fdopen(fd, 'w+b') as tmp:
                        # do stuff with temp file
                        tmp.write(chunk)
                    res = upload_post(name, file_id, upload_id, chunk_number, current_chunk_size, session)
                    if res and res.status_code == 200:
                        print("上传成功分片%d" % chunk_number)
                finally:
                    os.remove(name)
    else:
        chunk_number = 1
        current_chunk_size = total_size
        # 总的文件大小小于分片大小，直接就是1片
        res = upload_post(path, file_id, upload_id, chunk_number, current_chunk_size, session)
        if res and res.status_code == 200:
            print("上传成功")
        else:
            return "上传失败"
    # 发送合并分片请求
    res = complete_upload_file(file_id, upload_id, session)
    if res and res.status_code == 200:
        return "上传成功"
    else:
        return "上传失败"


def upload_get(identifier, pi, file_name, total_size, total_chunks, session):
    """
    第一次请求获取upload_id,是否上传过文件，以及上传过的分片id
    """
    # url = "http://202.109.131.111:8012/api/v1.0/files/chunk/upload"
    # url = "http://202.109.131.111:8018/api/v1.0/files/chunk/upload"
    # url = "http://172.24.3.80:5000/api/v1.0/files/chunk/upload"
    url = base_url + "api/v1.0/files/chunk/upload"
    data = {
        "identifier": identifier,
        "pi": pi,
        "filename": file_name,
        "totalSize": total_size,
        "totalChunks": total_chunks
    }
    r = requests.get(url, params=data, headers={"Cookie": session})
    return r


def upload_post(path, file_id, upload_id, chunk_number, current_chunk_size, session):
    """
        上传分片到服务器
    """
    # url = "http://202.109.131.111:8012/api/v1.0/files/chunk/upload"
    # url = "http://202.109.131.111:8018/api/v1.0/files/chunk/upload"
    # url = "http://172.24.3.80:5000/api/v1.0/files/chunk/upload"
    url = base_url + "api/v1.0/files/chunk/upload"
    files = {'file': (open(path, 'rb'))}
    data = {
        "file_id": file_id,
        "upload_id": upload_id,
        "chunkNumber": chunk_number,
        "currentChunkSize": current_chunk_size
    }
    res = requests.post(url, data=data, files=files, headers={"Cookie": session})
    return res


def get_file_md5(filename):
    file_hash = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            file_hash.update(b)
    return file_hash.hexdigest()


def complete_upload_file(file_id, upload_id, session):
    """
    合并分片的请求
    """
    # url = "http://202.109.131.111:8012/api/v1.0/files/complete_upload"
    # url = "http://202.109.131.111:8018/api/v1.0/files/complete_upload"
    # url = "http://172.24.3.80:5000/api/v1.0/files/complete_upload"
    url = base_url + "api/v1.0/files/complete_upload"
    data = {
        "file_id": file_id,
        "upload_id": upload_id
    }
    res = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json",
                                                             "Cookie": session})
    return res


def main(session, pi, path):
    chunk_size = 104857600  # 100M
    # pi = None
    # path = None
    session = session
    # try:
    #     options, args = getopt.getopt(argv, "hs:i:p:", ["help", "session=", "id=", "path="])
    # except getopt.GetoptError:
    #     sys.exit()
    # for option, value in options:
    #     if option in ("-h", "--help"):
    #         print("-s -----身份凭证")
    #         print("-i -----目标地址ID")
    #         print("-p -----文件路径")
    #         return "help"
    #     if option in ("-s", "--session"):
    #         session = "session=" + value
    #     if option in ("-i", "--id"):
    #         pi = value
    #     if option in ("-p", "--path"):
    #         path = value
    # if not all([session, pi, path]):
    #     return "参数不完整"
    result = file_chunk_spilt(path, chunk_size, pi, session)
    return result


if __name__ == '__main__':
    # s = 104857600
    # path = '/data/hxl/test/下载.jpg'
    # path = 'C:\\Users\\EDZ\\Desktop\\下载.jpg'
    # path = 'C:\\Users\\EDZ\\Downloads\\VID_20211219_121111.mp4'
    # pi = "root"
    # r = file_chunk_spilt(path, s, pi)
    # print(r)
    # session = "1edaeaa2-adf9-4073-bbf8-58869ced3ba1"
    # res = main(sys.argv[1:])
    print("-----------")


