import tempfile

import requests as r
from jinja2 import FileSystemLoader, Environment, select_autoescape

from tncli.modules.utils.system.conf import toncenter, project_root
import base64


def get_transactions(network: str, smc_address: str, logical_time: str, tx_hash: str):
    """Download transaction and run it locally"""

    tx_hash = tx_hash.upper()
    answer = r.get(
        f"{toncenter[network]}/getTransactions?address={smc_address}&limit=1&lt={logical_time}&hash={tx_hash}&archival=true")
    result = answer.json()["result"][0]
    msg_value = int(result["in_msg"]["value"])

    tx = base64.b64decode(result["data"]).hex().upper()

    message = base64.b64decode(result["in_msg"]["msg_data"]["body"]).hex().upper()

    loader = FileSystemLoader(f"{project_root}/modules/fift")

    env = Environment(
        loader=loader,
        autoescape=select_autoescape()
    )

    template = env.get_template("transaction_debug.fif.template")

    render_kwargs = {
        'tx_hex': tx,
        'message_hex': message,
        'msg_value': msg_value
    }

    rendered = template.render(**render_kwargs)
    to_save_location: str = tempfile.mkstemp(suffix='.fif')[1]

    with open(to_save_location, 'w') as f:
        f.write(rendered)

    # msg_value = int(res["in_msg"]["value"])
    # with open("tx.boc", "wb") as f:
    #     f.write(base64.b64decode(res["data"]))
    # with open("message.boc", "wb") as f:
    #     f.write(base64.b64decode(res["in_msg"]["msg_data"]["body"]))
    # with open("temp_script", "w") as f:
    #     f.write('"tx.boc" file>B B>boc <s ref@ <s ref@ 2 boc+>B "message_cell.boc" B>file')
    # os.system("fift temp_script")


if __name__ == "__main__":
    get_transactions('testnet', 'EQB36_EfYjFYMV8p_cxSYX61bA0FZ4B65ZNN6L8INY-5gL6w', '8640072000001',
                     'c381cb3ce303812ae2dbda4cd074494fb446877b708c3acb3c3da77ea7f78e7c')
