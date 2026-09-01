from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import tempfile

from app.db.database import SessionLocal, Base, engine

# Import all models so SQLAlchemy knows about them
from app.models.business import Business
from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale

# Create database tables
Base.metadata.create_all(bind=engine)

from app.services.insights_service import get_business_insights
from app.services.import_service import import_business_file

from app.schemas.business import (
    BusinessCreate,
    BusinessResponse,
)

from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
)

from app.schemas.product import (
    ProductCreate,
    ProductResponse,
)

from app.schemas.sale import (
    SaleCreate,
    SaleResponse,
)

from app.schemas.ask import (
    AskRequest,
    AskResponse,
)

from app.services.business_service import (
    create_business,
    get_businesses,
)

from app.services.customer_service import (
    create_customer,
    get_customers,
)

from app.services.product_service import (
    create_product,
    get_products,
)

from app.services.sale_service import (
    create_sale,
    get_sales,
)

from app.services.ask_service import (
    answer_business_question,
)

from app.services.business_query_service import (
    get_business_metrics,
    get_business_analytics,
)

from app.services.business_summary_service import (
    get_business_summary,
)


app = FastAPI(
    title="AI Business Assistant",
    description="AI-powered business knowledge and question-answering system",
    version="0.1.0",
)


# -------------------------
# CORS Configuration
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-business-assistant-1-n11w.onrender.com",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Database Dependency
# -------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# -------------------------
# Basic APIs
# -------------------------

@app.get("/")
def root():
    return {
        "message": "AI Business Assistant is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# -------------------------
# Business APIs
# -------------------------

@app.post(
    "/businesses",
    response_model=BusinessResponse,
)
def create_business_endpoint(
    business: BusinessCreate,
    db: Session = Depends(get_db),
):
    return create_business(db, business)


@app.get(
    "/businesses",
    response_model=list[BusinessResponse],
)
def list_businesses(
    db: Session = Depends(get_db),
):
    return get_businesses(db)


# -------------------------
# Business Metrics
# -------------------------

@app.get(
    "/businesses/{business_id}/metrics"
)
def business_metrics(
    business_id: int,
    db: Session = Depends(get_db),
):
    return get_business_metrics(
        db,
        business_id,
    )


# -------------------------
# Business Analytics
# -------------------------

@app.get(
    "/businesses/{business_id}/analytics"
)
def business_analytics(
    business_id: int,
    db: Session = Depends(get_db),
):
    return get_business_analytics(
        db,
        business_id,
    )


# -------------------------
# Business Insights
# -------------------------

@app.get(
    "/businesses/{business_id}/insights"
)
def business_insights(
    business_id: int,
    db: Session = Depends(get_db),
):
    return get_business_insights(
        db=db,
        business_id=business_id,
    )


# -------------------------
# Business Summary
# -------------------------

@app.get(
    "/businesses/{business_id}/summary"
)
def business_summary(
    business_id: int,
    db: Session = Depends(get_db),
):
    return get_business_summary(
        db,
        business_id,
    )


# -------------------------
# Excel / CSV Upload
# -------------------------

@app.post(
    "/businesses/{business_id}/upload"
)
async def upload_business_data(
    business_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    allowed_extensions = {
        ".xlsx",
        ".xls",
        ".csv",
    }

    filename = file.filename or ""

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid file type. "
                "Please upload an Excel or CSV file."
            ),
        )

    temp_path = None

    try:
        file_content = await file.read()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temp_file:

            temp_file.write(file_content)

            temp_path = temp_file.name

        result = import_business_file(
            db=db,
            business_id=business_id,
            file_path=temp_path,
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Import failed: {str(error)}",
        )

    finally:

        if temp_path and os.path.exists(
            temp_path
        ):
            os.remove(temp_path)


# -------------------------
# Customer APIs
# -------------------------

@app.post(
    "/customers",
    response_model=CustomerResponse,
)
def create_customer_endpoint(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
):
    return create_customer(
        db,
        customer,
    )


@app.get(
    "/customers",
    response_model=list[CustomerResponse],
)
def list_customers(
    db: Session = Depends(get_db),
):
    return get_customers(db)


# -------------------------
# Product APIs
# -------------------------

@app.post(
    "/products",
    response_model=ProductResponse,
)
def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    return create_product(
        db,
        product,
    )


@app.get(
    "/products",
    response_model=list[ProductResponse],
)
def list_products(
    db: Session = Depends(get_db),
):
    return get_products(db)


# -------------------------
# Sales APIs
# -------------------------

@app.post(
    "/sales",
    response_model=SaleResponse,
)
def create_sale_endpoint(
    sale: SaleCreate,
    db: Session = Depends(get_db),
):
    return create_sale(
        db,
        sale,
    )


@app.get(
    "/sales",
    response_model=list[SaleResponse],
)
def list_sales(
    db: Session = Depends(get_db),
):
    return get_sales(db)


# -------------------------
# AI Assistant
# -------------------------

@app.post(
    "/ask",
    response_model=AskResponse,
)
def ask_business_question(
    request: AskRequest,
    db: Session = Depends(get_db),
):
    answer = answer_business_question(
        db=db,
        business_id=request.business_id,
        question=request.question,
    )

    return {
        "answer": answer
    }