import random
import time
import eth_account.signers.local
import web3
from web3 import Web3, Account
from config import RPC_URL, CONTRACT_ADDRESS, CONTRACT_METHOD, CHAIN_ID


def get_logo():
    print("""
███╗   ██╗ ██████╗ ██████╗ ███████╗██████╗ ██╗   ██╗███╗   ██╗███╗   ██╗███████╗██████╗ 
████╗  ██║██╔═══██╗██╔══██╗██╔════╝██╔══██╗██║   ██║████╗  ██║████╗  ██║██╔════╝██╔══██╗
██╔██╗ ██║██║   ██║██║  ██║█████╗  ██████╔╝██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██║╚██╗██║██║   ██║██║  ██║██╔══╝  ██╔══██╗██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║ ╚████║╚██████╔╝██████╔╝███████╗██║  ██║╚██████╔╝██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝

Подписаться на канал may.crypto{🦅}, чтобы быть в курсе самых актуальных нод - https://t.me/maycrypto
""")


def menu() -> int:
    x = None
    while not x:
        print("""
1) Ввести seed-фразу
2) Сгенерировать и использовать новый кошелек
3) Использовать Private Key
        """)
        x = input("-> ")
    return int(x)


def get_account_from_seed(w3: web3.Web3) -> eth_account.signers.local.LocalAccount:
    w3.eth.account.enable_unaudited_hdwallet_features()
    print("Введите Вашу seed-фразу: ")
    phrase = input("-> ")
    try:
        account = w3.eth.account.from_mnemonic(phrase)
        print(f"Адрес Вашего кошелька: {account.address}")
        return account
    except Exception as e:
        print(e)
        main()


def get_account_from_pk(w3: web3.Web3) -> eth_account.signers.local.LocalAccount:
    w3.eth.account.enable_unaudited_hdwallet_features()
    print("Введите Ваш приватный ключ")
    pk = input("-> ")
    try:
        account = w3.eth.account.from_key(pk)
        print(f"Адрес Вашего кошелька: {account.address}")
        return account
    except Exception as e:
        print(e)
        main()


def generate_account(w3: web3.Web3) -> eth_account.signers.local.LocalAccount:
    w3.eth.account.enable_unaudited_hdwallet_features()
    print("Генерирую новый кошелек...")
    account, mnemonic = w3.eth.account.create_with_mnemonic()
    print(f"Адрес Вашего кошелька: {account.address}")
    print(f"Seed фраза Вашего кошелька: {mnemonic}")
    print(f"Приватный ключ Вашего кошелька: {account.key.hex()}")
    return account


def check_eth_balance(w3: web3.Web3, account: eth_account.signers.local.LocalAccount):
    balance = w3.from_wei(w3.eth.get_balance(account.address), "ether")
    print(f"Баланс Вашего кошелька: {balance} ETH")
    if balance < 0.00001:
        print("Запросите средства на кошелек по ссылке:")
        print("https://rivalz2.hub.caldera.xyz/")
        print("")
        input("После чего нажмите Enter")
    else:
        input("Нажмите Enter для запуска авто-клейма")


def claim_nft(w3: web3.Web3, account: eth_account.signers.local.LocalAccount):
    nonce = w3.eth.get_transaction_count(account.address)

    # Автоматический расчет цены газа
    gas_price = w3.eth.gas_price

    # Фиксированный лимит газа, как было изначально
    gas_limit = 300000
    gas = w3.eth.gas

    transaction = {
        'to': CONTRACT_ADDRESS,
        'value': 0,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'data': CONTRACT_METHOD,
        'chainId': CHAIN_ID
    }

    try:
        signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"NFT claim hash: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка при выполнении транзакции: {e}")


def main() -> None:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if w3.is_connected():
        if (choice := menu()) == 1:
            account = get_account_from_seed(w3)
            check_eth_balance(w3, account)
        elif choice == 2:
            account = generate_account(w3)
            check_eth_balance(w3, account)
        elif choice == 3:
            account = get_account_from_pk(w3)
            check_eth_balance(w3, account)
        while True:
            print("Начинаем клейм...")
            for i in range(20):
                claim_nft(w3, account)
                print(f"{i + 1}й запрос на клейм отправлен успешно!")
                time.sleep(random.randint(5, 15))
            print("Ожидание 12 часов...")
            time.sleep(43260)
    else:
        print("Web3 connection failed!")
        print("Check your internet connection")


if __name__ == "__main__":
    get_logo()
    main()
