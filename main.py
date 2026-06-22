import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Revbox API", version="1.0.0")

# --- CORS -------------------------------------------------------------------
# In dev folosim Vite (5173). In productie, originea de pe Vercel vine din env.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Modele -----------------------------------------------------------------
class Product(BaseModel):
    id: int
    name: str
    category: str
    brand: str
    price: float  # RON
    short: str
    description: str
    specs: list[str]
    image: str
    stock: int


class CartItem(BaseModel):
    id: int
    qty: int


class Customer(BaseModel):
    name: str
    email: str
    phone: str
    address: str


class CheckoutRequest(BaseModel):
    items: list[CartItem]
    customer: Customer


class OrderLine(BaseModel):
    id: int
    name: str
    qty: int
    price: float
    subtotal: float


class OrderResponse(BaseModel):
    order_id: str
    status: str
    total: float
    items: list[OrderLine]


# --- Date produse (12 piese tuning/performance) -----------------------------
PRODUCTS: list[Product] = [
    Product(
        id=1,
        name="Sistem admisie sport cu filtru conic",
        category="Admisie",
        brand="RevFlow",
        price=649.0,
        short="Admisie aer rece pentru flux marit si raspuns mai bun la accelerare.",
        description=(
            "Kit de admisie sport care inlocuieste cutia de aer originala cu un filtru conic "
            "lavabil si o tubulatura din aluminiu. Creste fluxul de aer catre motor pentru un "
            "raspuns mai prompt si un sunet de admisie sportiv."
        ),
        specs=[
            "Filtru conic lavabil si reutilizabil",
            "Tubulatura aluminiu cu izolare termica",
            "Castig estimat: +5-8 CP",
            "Montaj plug-and-play, fara modificari",
        ],
        image="https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?auto=format&fit=crop&w=800&q=80",
        stock=24,
    ),
    Product(
        id=2,
        name="Evacuare cat-back inox",
        category="Evacuare",
        brand="RevFlow",
        price=2190.0,
        short="Linie de evacuare cat-back din inox 304 pentru sunet si flux superior.",
        description=(
            "Sistem complet cat-back din inox 304, cu tobe sport si tubulatura de diametru marit. "
            "Reduce contrapresiunea si ofera o nota de evacuare profunda, sportiva, fara a fi "
            "obositoare in croaziera."
        ),
        specs=[
            "Inox 304 rezistent la coroziune",
            "Diametru teava marit pentru flux liber",
            "Tobe cu sunet sportiv calibrat",
            "Terminale lustruite incluse",
        ],
        image="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80",
        stock=12,
    ),
    Product(
        id=3,
        name="Suspensie coilover reglabila",
        category="Suspensie",
        brand="ApexRide",
        price=3450.0,
        short="Coilovere cu reglaj de inaltime si amortizare pentru drum si pista.",
        description=(
            "Set de coilovere cu reglaj de inaltime si 32 de trepte de amortizare. Iti permite sa "
            "cobori masina si sa ajustezi comportamentul suspensiei pentru confort sau performanta "
            "pe circuit."
        ),
        specs=[
            "Reglaj inaltime independent",
            "32 trepte de amortizare",
            "Arcuri sport din otel calit",
            "Garnituri etansare pentru durabilitate",
        ],
        image="https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?auto=format&fit=crop&w=800&q=80",
        stock=8,
    ),
    Product(
        id=4,
        name="Kit Big Brake 6 pistoane",
        category="Franare",
        brand="StopTech Pro",
        price=4990.0,
        short="Etriere monobloc 6 pistoane si discuri ventilate pentru franare puternica.",
        description=(
            "Upgrade complet de franare cu etriere monobloc cu 6 pistoane si discuri ventilate de "
            "diametru mare. Reduce dramatic distanta de franare si rezista la fading in conditii "
            "intense de utilizare."
        ),
        specs=[
            "Etriere monobloc 6 pistoane",
            "Discuri ventilate 355 mm",
            "Placute performance incluse",
            "Furtune franare armate inox",
        ],
        image="https://images.unsplash.com/photo-1577133275877-2e1d3c8a8e0d?auto=format&fit=crop&w=800&q=80",
        stock=6,
    ),
    Product(
        id=5,
        name="Intercooler frontal aluminiu",
        category="Racire",
        brand="CoolCore",
        price=1750.0,
        short="Intercooler frontal de capacitate marita pentru temperaturi de admisie scazute.",
        description=(
            "Intercooler frontal din aluminiu cu miez bar-and-plate, proiectat pentru motoare "
            "turbo. Reduce temperatura aerului de admisie, mentine puterea constanta si previne "
            "pierderea de performanta la solicitari repetate."
        ),
        specs=[
            "Miez bar-and-plate de mare eficienta",
            "Constructie integral aluminiu sudat",
            "Conexiuni pentru montaj direct",
            "Scadere semnificativa a temperaturii de admisie",
        ],
        image="https://images.unsplash.com/photo-1632823471565-1ecdf5c6da77?auto=format&fit=crop&w=800&q=80",
        stock=10,
    ),
    Product(
        id=6,
        name="Downpipe sport cu decat",
        category="Evacuare",
        brand="RevFlow",
        price=1290.0,
        short="Downpipe de diametru marit care elibereaza fluxul de evacuare al turbinei.",
        description=(
            "Downpipe sport cu decatalizator care reduce contrapresiunea imediat dupa turbina. "
            "Imbunatateste spool-ul turbo si elibereaza putere suplimentara, mai ales in "
            "combinatie cu o remapare."
        ),
        specs=[
            "Inox 304, diametru marit",
            "Spool turbo mai rapid",
            "Pregatit pentru remapare Stage 1/2",
            "Flanse laser-cut pentru montaj precis",
        ],
        image="https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?auto=format&fit=crop&w=800&q=80",
        stock=14,
    ),
    Product(
        id=7,
        name="Bara stabilizatoare intarita",
        category="Suspensie",
        brand="ApexRide",
        price=890.0,
        short="Bara antiruliu mai rigida pentru reducerea inclinarii in viraje.",
        description=(
            "Bara stabilizatoare din otel intarit care reduce ruliul caroseriei in viraje. Ofera "
            "un comportament mai plat si mai previzibil, cu o aderenta imbunatatita pe ambele axe."
        ),
        specs=[
            "Otel intarit, rigiditate sporita",
            "Bucse poliuretan incluse",
            "Reduce ruliul in viraje",
            "Compatibila cu suspensii sport",
        ],
        image="https://images.unsplash.com/photo-1581093588401-fbb62a02f120?auto=format&fit=crop&w=800&q=80",
        stock=18,
    ),
    Product(
        id=8,
        name="Volant usor (flywheel)",
        category="Motor",
        brand="DriveTech",
        price=1450.0,
        short="Volant masa redusa pentru turatii mai vioaie si raspuns rapid.",
        description=(
            "Volant din otel cromat-molibden cu masa redusa, care permite motorului sa urce mai "
            "rapid in turatie. Ideal pentru un raspuns sportiv si schimbari de viteza mai prompte."
        ),
        specs=[
            "Otel cromat-molibden de inalta rezistenta",
            "Masa redusa pentru turatii vioaie",
            "Echilibrat dinamic din fabrica",
            "Compatibil cu ambreiaje performance",
        ],
        image="https://images.unsplash.com/photo-1537984822441-cff330075342?auto=format&fit=crop&w=800&q=80",
        stock=9,
    ),
    Product(
        id=9,
        name="Set bujii iridium performance",
        category="Motor",
        brand="SparkMax",
        price=320.0,
        short="Bujii cu electrod iridium pentru scanteie stabila si ardere eficienta.",
        description=(
            "Set de bujii cu electrod fin din iridium care asigura o scanteie puternica si "
            "constanta. Imbunatatesc arderea, raspunsul la accelerare si consumul, mai ales pe "
            "motoare modificate."
        ),
        specs=[
            "Electrod central din iridium",
            "Scanteie stabila la turatii mari",
            "Durata de viata extinsa",
            "Set complet pentru 4 cilindri",
        ],
        image="https://images.unsplash.com/photo-1517524206127-48bbd363f3d7?auto=format&fit=crop&w=800&q=80",
        stock=40,
    ),
    Product(
        id=10,
        name="Distantiere roti (wheel spacers)",
        category="Roti",
        brand="TrakWidth",
        price=380.0,
        short="Distantiere din aluminiu pentru ecartament marit si aspect agresiv.",
        description=(
            "Set de distantiere din aluminiu forjat care maresc ecartamentul rotilor. Imbunatatesc "
            "stabilitatea in viraje si ofera masinii un aspect mai agresiv, cu rotile aliniate la "
            "marginea aripii."
        ),
        specs=[
            "Aluminiu forjat de inalta rezistenta",
            "Prezoane si suruburi incluse",
            "Ecartament marit pentru stabilitate",
            "Centrare hub pentru montaj precis",
        ],
        image="https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=800&q=80",
        stock=22,
    ),
    Product(
        id=11,
        name="Eleron carbon",
        category="Aerodinamica",
        brand="AeroForm",
        price=1690.0,
        short="Eleron din fibra de carbon pentru apasare aerodinamica si stil.",
        description=(
            "Eleron spate din fibra de carbon real, cu finisaj lucios. Adauga apasare aerodinamica "
            "la viteze mari pentru o stabilitate sporita, completand totodata aspectul sportiv al "
            "masinii."
        ),
        specs=[
            "Fibra de carbon reala, finisaj lucios",
            "Apasare aerodinamica la viteza mare",
            "Suporti din aluminiu inclusi",
            "Kit complet de prindere",
        ],
        image="https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80",
        stock=7,
    ),
    Product(
        id=12,
        name="Kit silentblocuri poliuretan",
        category="Suspensie",
        brand="ApexRide",
        price=540.0,
        short="Bucse poliuretan pentru precizie sporita a directiei si suspensiei.",
        description=(
            "Set complet de silentblocuri din poliuretan care inlocuiesc bucsele de cauciuc uzate. "
            "Reduc jocul in suspensie, cresc precizia directiei si imbunatatesc feedback-ul de la "
            "drum."
        ),
        specs=[
            "Poliuretan rezistent la uzura",
            "Precizie sporita a directiei",
            "Kit complet pentru ambele axe",
            "Vaselina de montaj inclusa",
        ],
        image="https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=800&q=80",
        stock=16,
    ),
]

PRODUCTS_BY_ID: dict[int, Product] = {p.id: p for p in PRODUCTS}


# --- Endpoints --------------------------------------------------------------
@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/products", response_model=list[Product])
def list_products():
    return PRODUCTS


@app.get("/api/categories", response_model=list[str])
def list_categories():
    # Categorii distincte, in ordinea aparitiei.
    seen: list[str] = []
    for p in PRODUCTS:
        if p.category not in seen:
            seen.append(p.category)
    return seen


@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = PRODUCTS_BY_ID.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produsul nu a fost gasit")
    return product


@app.post("/api/checkout", response_model=OrderResponse)
def checkout(req: CheckoutRequest):
    if not req.items:
        raise HTTPException(status_code=400, detail="Cosul este gol")

    lines: list[OrderLine] = []
    total = 0.0
    for item in req.items:
        product = PRODUCTS_BY_ID.get(item.id)
        if product is None:
            raise HTTPException(
                status_code=400, detail=f"Produsul {item.id} nu exista"
            )
        if item.qty < 1:
            raise HTTPException(
                status_code=400, detail=f"Cantitate invalida pentru {product.name}"
            )
        if item.qty > product.stock:
            raise HTTPException(
                status_code=400,
                detail=f"Stoc insuficient pentru {product.name}",
            )
        # Pretul vine din server, nu de la client.
        subtotal = round(product.price * item.qty, 2)
        total += subtotal
        lines.append(
            OrderLine(
                id=product.id,
                name=product.name,
                qty=item.qty,
                price=product.price,
                subtotal=subtotal,
            )
        )

    return OrderResponse(
        order_id=f"RVB-{uuid.uuid4().hex[:8].upper()}",
        status="confirmed",
        total=round(total, 2),
        items=lines,
    )
