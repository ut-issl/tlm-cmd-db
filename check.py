import argparse
from modules.csv2toml import Csv2TomlTLM, Csv2TomlCMD
from modules.toml2mdcsv import Toml2MdCsvTLM, Toml2MdCsvCMD
from modules.checktoml import CheckTomlTLM, CheckTomlCMD
from modules.utils import status2md, checksettings


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--obc", help='choose obc')
    parser.add_argument("-i", "--input", help='(optional) input csv file/dir path, only tlm_db is allowed')
    parser.add_argument("-t", "--toml", type=str, help="toml dest dir path")
    parser.add_argument("-m", "--md", type=str, help="md dest dir path")
    parser.add_argument("-c", "--csv", type=str, help="csv dest dir path")
    parser.add_argument('--tlm', action='store_true', help="(optional) check only tlm_db")
    parser.add_argument('--cmd', action='store_true', help="(optional) check only cmd_db")
    opt = parser.parse_args()
    if opt.input is not None:
        if not opt.tlm and not opt.cmd:
            raise ValueError("既存のcsvをtomlに変換する場合は, --tlmか--cmdを指定してください. ")
        if opt.obc is None:
            raise ValueError("既存のcsvをtomlに変換する場合は, obcを指定してください. \nex) --obc mobc")
    if (opt.toml is not None or opt.md is not None or opt.csv is not None) and (not opt.tlm or not opt.cmd):
        raise ValueError("--csv, --md, --tomlでディレクトリを指定する場合には--tlmか--cmdを明示してください")
    if opt.cmd and opt.tlm:
        raise ValueError("--cmdと--tlmは片方のみ指定可能です.")
    return opt


def main(opt):
    opt = checksettings(opt)
    if opt.input is not None:
        if opt.is_tlm:
            print("START csv to toml")
            Csv2TomlTLM(path_to_csv=opt.input, path_to_toml=opt.tlm_toml, obc=opt.obc)
            print("END csv to toml end")
            return
        if opt.is_cmd:
            print("START csv to toml")
            Csv2TomlCMD(path_to_csv=opt.input, path_to_toml=opt.cmd_toml, obc=opt.obc)
            print("END csv to toml end")
            return
    if opt.is_tlm:
        status2md()
        print("START check tlm toml")
        CheckTomlTLM(path_to_toml=opt.tlm_toml)
        print("END check toml")
        print("START tlm toml to md&csv")
        Toml2MdCsvTLM(path_to_toml=opt.tlm_toml, path_to_md=opt.tlm_md, path_to_csv=opt.tlm_csv)
        print("END tlm toml to md&csv")
    if opt.is_cmd:
        print("START check cmd toml")
        CheckTomlCMD(path_to_toml=opt.cmd_toml)
        print("END check cmd toml")
        print("START cmd toml to md&csv")
        Toml2MdCsvCMD(path_to_toml=opt.cmd_toml, path_to_md=opt.cmd_md, path_to_csv=opt.cmd_csv)
        print("END toml to md&csv")


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
