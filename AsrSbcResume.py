
from AsrContrasts.SBC import Sbc as SbcRunClient




if __name__ == '__main__':
    # get_result()
    # insertcase()
    #     data_list='''e10f1ef9ee4188fb9354651a48be98f8_20200831161944_e3758539-12de-4182-b104-69d103b5cf5d.wav
    # e86c7e26-7716-4fea-9406-501fe4621d35_20200831131932_801775b8-513a-4513-b3ff-4b3f7f9fdd6b.wav
    # b4c3115b-6d0b-4d3a-a881-e0d7455976de_20200831114507_c00ebde6-9057-4af1-915d-1bbc12068fd8.wav'''.splitlines()
    #     dir = '/home/kangyong/Data/wav'
    # run_asr()
    sbc = SbcRunClient('AsrEngineResult20200911173923', '/mnt/20200831_wav')
    sbc.resume()
