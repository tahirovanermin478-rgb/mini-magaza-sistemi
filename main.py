

# 1. Faylları hazırlayan funksiya
def fayllari_yarat():
    if not os.path.exists("users.json"):
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump([{"username": "student1", "password": "1234", "balance": 100.0, "lock": 0}], f)
    if not os.path.exists("products.json"):
        with open("products.json", "w", encoding="utf-8") as f:
            json.dump({"Məhsullar": [{"id": 1, "name": "Köynək", "price": 20}, {"id": 2, "name": "Şalvar", "price": 40}]}, f)

# 2. Giriş sistemi
def login():
    fayllari_yarat()
    u_name = input("İstifadəçi adı: ")
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
    
    user = next((u for u in users if u["username"] == u_name), None)
    if not user: print("İstifadəçi tapılmadı!"); return None
    
    if user["lock"] > time.time():
        print(f"Blokdasınız! {int(user['lock'] - time.time())} san gözləyin."); return None

    sifre = input("Şifrə: ")
    if user["password"] == sifre:
        print("Xoş gəldiniz!"); return user
    else:
        print("Səhv şifrə! 10 saniyə bloklandınız."); user["lock"] = time.time() + 10
        with open("users.json", "w", encoding="utf-8") as f: json.dump(users, f)
        return None

# 3. Mağaza menyusu
def menyu(u):
    sebet = []
    while True:
        print(f"\nBalans: {u['balance']} AZN")
        secim = input("1. Məhsullar\n2. Səbət\n0. Çıxış\nSeçim: ")
        
        if secim == "1":
            with open("products.json", "r", encoding="utf-8") as f: prods = json.load(f)
            for m in prods["Məhsullar"]: print(f"ID: {m['id']} | {m['name']} - {m['price']} AZN")
            m_id = input("Səbətə atmaq üçün ID seçin (Geri üçün 0): ")
            if m_id != "0":
                item = next((i for i in prods["Məhsullar"] if str(i["id"]) == m_id), None)
                if item: sebet.append(item); print("Səbətə əlavə olundu!")
        
        elif secim == "2":
            toplam = sum(i["price"] for i in sebet)
            print(f"Səbət toplamı: {toplam} AZN")
            if toplam > 0 and input("Almaq istəyirsiniz? (h/y): ") == "h":
                if u["balance"] >= toplam:
                    u["balance"] -= toplam; sebet.clear(); print("Alındı!")
                else: print("Balans çatmır!")
        elif secim == "0": break

# İşə salırıq
istifadeci = login()
if istifadeci: menyu(istifadeci)

