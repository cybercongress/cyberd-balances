# Install

```bash
pip3 install -r ./requirements.txt
```

# Run

Create ethereum snapshot CSV with balances
```bash
python3 ./src/ethereum_snapshot.py --block ACTUAL_BLOCK
```

Create cosmos snapshot CSV with balances
```bash
python3 ./src/cosmos_hub_snapshot.py
```

Create merged genesis file
```bash
python3 ./src/genesis_generator.py
```

# Distribution / Prepare scripts task

![](flow.png)

Задача - сформировать генезис файл **genesis.json**, добавив в него аккаунты и рассчитанные балансы.
Стартовый генезис файл без балансов - **network_genesis.json**

Пример структуры для добавления:
```
"accounts": [
      {
        "addr": "cyber1qqqqqqqqqqqqqqqqqqqqqqqqqqqqph4djv52fh",
        "amt": "1180000000000001",
        "nmb": "132317"
      },
      {
        "addr": "cyber1qqqr2yuufayq6hytrqta6sutu7n6yt6vas8rqu",
        "amt": "60123874985",
        "nmb": "99119"
      }
]
```

Общая эмиссия сайбов - **1000000000000000** (1 квадриллион)

Скрипт **ethereum_snapshot.py** 
- забирает с big query стейт аккаунтов 
- дает на выходе CSV файл аккаунтов с балансами (аккаунты с общей суммой стейка в 80% от эмиссии эфира за исключением контрактов)

Скрипт **cosmos_hub_snapshot.py** 
- принимает на вход экспортированный стейт космос хаба (экспорт на определенном блоке) в виде файла **cosmos_genesis_snapshot.json** 
- дает на выходе CSV файл с аккаунтами и балансами **cosmos.csv**, меняет **префикс адреса с cosmos на cyber**

Скрипт **genesis_generator.py**
- принимает на вход файл **ethereum.csv** 
- принимает на вход файл **cosmos.csv** 
- принимает на вход файл **network_genesis.json** - в него в путь **accounts**  внутри файла **network_genesis.json** будут вставляться аккаунты и рассчитанные балансы
- принимает на вход файл **cyber_distribution.json**, в нем указаны **проценты аллокации балансов**
```
{
    "inventors": "2",
    "cybercongress": "4",
    "investors": "4",
    "cosmos_drop": "5",
    "ethereum_drop": "10",
    "pre_genesis_round": "5",
    "game_of_thrones": "20",
    "foundation_auction_multisig": "60"
}
```
1. Аккаунтам из **ethereum.csv** идет **ethreum_drop процент**
2. Аккаунтам из **cosmos.csv** идет **cosmos_drop процент**
- принимает на вход файл **manual_distribution.json**, который содержит в себе информацию об аллокации на конкретные адреса и процентами внутри группы.
```
{
    "inventors": {
        "cyber1lle7ul44h9xqh8k7hesm5w966jljrr5dwkeghr": "50",
        "cyber1ll67af9cs0jj82rml08kpn25yd77sr0e55e7ur": "50"
    },
    "cybercongress": {
        "cyber1llm6upvjadgrt8pq4h32lgmezw8fwwnl5g6s9r": "100",
    },
    "investors": {
        "cyber1lldfm9h9psqawxv3fk44jvc73wwpl0nu68zyql": "75",
        "cyber1llmtzud92cxtky50ruuv6t3mrmxf6kafq4eqya": "10",
        "cyber1lluqd4vdxrrwsgpa3h2amrfkxf39csaeefn6wq": "5",
        "cyber1lls6mrzd6zqqs0sguj050r9t68egafe0p633gm": "5",
        "cyber1llnkr9fa6jcyz0zgyplmlhyr7njhumk5n8ergg": "5",
    },
    "pre_genesis_round": {
        "cyber1qq2jnn3vhlzu368cxvfr8vzerwsd2fgwqxkgec": "100",
    },
    "game_of_thrones": {
        "cyber1llt3rp80fvlc40e5vm9sc5x49uv8vsnr5kv7qr": "50",
        "cyber1lltdurdnh3au6aytek8cg2ppzhjlzp7g5fvenq": "50"
    },
    "foundation_auction_multisig": {
        "cyber1lldzw0m4fhlsqtwf5gd5rp59ywfqlvanyc8k0u": "100",
    }
}
```

1. **И сохраняет все в файл genesis.json**
2. **Одни и теже аккаунты могут находится в разных группах, нужно суммировать конечные балансы**
3. **Необходима проверка суммы балансов всех аккаунтов с общим суплаем**
4. **Для аккаунтов из manual_distribution нумерация начинается в первую очередь - это значит что эти аккаунты будут находится вверху accounts**
4. Большие файлы отлично открываются в Sublime Text
