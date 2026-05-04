# 1. Faylları və ilkin məlumatları yaradırıq
if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump([{"username": "student1", "password": "1234", "balance": 100.0, "lock": 0}], f)

if not os.path.exists("products.json"):
    with open("products.json", "w") as f:
        json.dump({"Geyimler": [{"id": 1, "name": "T-Shirt", "price": 12.5}]}, f)

# 2. Giriş (Login) və 10 saniyəlik blok sistemi
print("=== GİRİŞ ===")
u_name = input("İstifadəçi adı: ")
sifre = input("Şifrə: ")

with open("users.json", "r") as f:
    users = json.load(f)

user = None
for u in users:
    if u["username"] == u_name:
        user = u

if not user:
    print("İstifadəçi tapılmadı!")
    exit()

if user["lock"] > time.time():
    print(f"Bloklanmısınız! {int(user['lock'] - time.time())} saniyə gözləyin.")
    exit()

if user["password"] != sifre:
    print("Şifrə səhvdir! 10 saniyəlik bloklandınız.")
    user["lock"] = time.time() + 10
    with open("users.json", "w") as f:
        json.dump(users, f)
    exit()

print(f"\nXoş gəldiniz, {user['username']}!")

# 3. Sadə Səbət Sistemi
basket = []

# 4. Əsas Menyu
while True:
    print(f"\nBalans: {user['balance']} AZN")
    print("1. Məhsullara bax və Səbətə at")
    print("2. Səbətimə bax və Alış-veriş et (Checkout)")
    print("0. Çıxış")
    
    secim = input("Seçin: ")
    
    if secim == "1":
        with open("products.json", "r") as f:
            prods = json.load(f)
        print("\n--- MƏHSULLAR ---")
        for k, v in prods.items():
            for m in v:
                print(f"ID: {m['id']} | {m['name']} - {m['price']} AZN")
        
        m_id = input("Səbətə atmaq üçün ID seçin (Geri üçün 0): ")
        if m_id == "1":
            basket.append(prods["Geyimler"][0])
            print("T-Shirt səbətə əlavə olundu!")
            
    elif secim == "2":
        print("\n--- SƏBƏTİNİZ ---")
        if not basket:
            print("Səbətiniz boşdur.")
        else:
            cem = 0
            for b in basket:
                print(f"- {b['name']}: {b['price']} AZN")
                cem += b["price"]
            print(f"Toplam: {cem} AZN")
            
            al = input("Almaq istəyirsiniz? (beli/xeyr): ")
            if al.lower() == "beli":
                if user["balance"] >= cem:
                    user["balance"] -= cem
                    print(f"Alış-veriş tamamlandı! Yeni balans: {user['balance']} AZN")
                    basket.clear()
                    # Balansı faylda yeniləyirik
                    with open("users.json", "w") as f:
                        json.dump(users, f)
                else:
                    print("Balansınız çatmır!")
                    
    elif secim == "0":
        print("Sağ olun!")
        break
