const API_URL = "https://ai-business-assistant-lc4m.onrender.com";

let businessId = 3;

// =========================
// DOM Elements
// =========================

const questionInput =
document.getElementById("question");

const askButton =
document.getElementById("ask-button");

const answerBox =
document.getElementById("answer");

const customerCount =
document.getElementById("customer-count");

const productCount =
document.getElementById("product-count");

const salesCount =
document.getElementById("sales-count");

const revenue =
document.getElementById("revenue");

const averageSale =
document.getElementById("average-sale");

const quantitySold =
document.getElementById("quantity-sold");

const insightsBox =
document.getElementById("insights");

const topProductsBox =
document.getElementById("top-products");

const topCustomersBox =
document.getElementById("top-customers");

// =========================
// Business Setup Elements
// =========================

const businessNameInput =
document.getElementById("business-name");

const businessIndustryInput =
document.getElementById("business-industry");

const businessDescriptionInput =
document.getElementById("business-description");

const createBusinessButton =
document.getElementById("create-business-button");

const businessMessage =
document.getElementById("business-message");

// =========================
// Upload Elements
// =========================

const businessFileInput =
document.getElementById("business-file");

const uploadButton =
document.getElementById("upload-button");

const uploadMessage =
document.getElementById("upload-message");

// =========================
// Customer Form
// =========================

const customerNameInput =
document.getElementById("customer-name");

const customerEmailInput =
document.getElementById("customer-email");

const addCustomerButton =
document.getElementById("add-customer-button");

const customerMessage =
document.getElementById("customer-message");

// =========================
// Product Form
// =========================

const productNameInput =
document.getElementById("product-name");

const productPriceInput =
document.getElementById("product-price");

const addProductButton =
document.getElementById("add-product-button");

const productMessage =
document.getElementById("product-message");

// =========================
// Sale Form
// =========================

const saleProductIdInput =
document.getElementById("sale-product-id");

const saleCustomerIdInput =
document.getElementById("sale-customer-id");

const saleQuantityInput =
document.getElementById("sale-quantity");

const addSaleButton =
document.getElementById("add-sale-button");

const saleMessage =
document.getElementById("sale-message");

// =========================
// Format Error
// =========================

function formatError(error) {

if (!error) {
    return "Something went wrong.";
}

if (error.message) {
    return error.message;
}

return String(error);


}

// =========================
// Format Currency
// =========================

function formatCurrency(value) {

return `₹${Number(value || 0).toLocaleString(
    "en-IN",
    {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }
)}`;

}

// =========================
// Load Business Metrics
// =========================

async function loadBusinessMetrics() {

try {

    const response =
        await fetch(
            `${API_URL}/businesses/${businessId}/summary`
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to load business summary"
        );
    }


    // Customers

    if (customerCount) {

        customerCount.textContent =
            data.customer_count ?? 0;
    }


    // Products

    if (productCount) {

        productCount.textContent =
            data.product_count ?? 0;
    }


    // Sales

    if (salesCount) {

        salesCount.textContent =
            data.total_sales ?? 0;
    }


    // Revenue

    if (revenue) {

        revenue.textContent =
            formatCurrency(
                data.total_revenue
            );
    }


    // Average Sale

    if (averageSale) {

        averageSale.textContent =
            formatCurrency(
                data.average_sale_value
            );
    }


    // Quantity Sold

    if (quantitySold) {

        quantitySold.textContent =
            data.total_quantity_sold ?? 0;
    }


} catch (error) {

    console.error(
        "Business summary error:",
        error
    );


    if (customerCount) {
        customerCount.textContent = "-";
    }

    if (productCount) {
        productCount.textContent = "-";
    }

    if (salesCount) {
        salesCount.textContent = "-";
    }

    if (revenue) {
        revenue.textContent = "-";
    }

    if (averageSale) {
        averageSale.textContent = "-";
    }

    if (quantitySold) {
        quantitySold.textContent = "-";
    }
}

}

// =========================
// Load Business Analytics
// =========================

async function loadBusinessAnalytics() {

/*
 * IMPORTANT:
 * If the analytics HTML elements do not exist,
 * simply skip analytics instead of crashing
 * the entire application.
 */

if (
    !topProductsBox ||
    !topCustomersBox
) {

    console.warn(
        "Analytics elements not found. Skipping analytics."
    );

    return;
}


try {

    const response =
        await fetch(
            `${API_URL}/businesses/${businessId}/analytics`
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to load business analytics"
        );
    }


    // =========================
    // Top Products
    // =========================

    topProductsBox.innerHTML = "";


    if (
        !data.top_products ||
        data.top_products.length === 0
    ) {

        const message =
            document.createElement("p");

        message.className =
            "analytics-loading";

        message.textContent =
            "No product sales available yet.";

        topProductsBox.appendChild(
            message
        );

    } else {

        data.top_products.forEach(
            function (product, index) {

                const item =
                    document.createElement("div");

                item.className =
                    "analytics-item";


                const left =
                    document.createElement("div");


                const name =
                    document.createElement("div");

                name.className =
                    "analytics-name";

                name.textContent =
                    `${index + 1}. ${product.product_name}`;


                const details =
                    document.createElement("div");

                details.className =
                    "analytics-details";

                details.textContent =
                    `${product.quantity_sold} units sold`;


                left.appendChild(name);

                left.appendChild(details);


                const right =
                    document.createElement("div");

                right.className =
                    "analytics-revenue";

                right.textContent =
                    formatCurrency(
                        product.revenue
                    );


                item.appendChild(left);

                item.appendChild(right);


                topProductsBox.appendChild(
                    item
                );
            }
        );
    }


    // =========================
    // Top Customers
    // =========================

    topCustomersBox.innerHTML = "";


    if (
        !data.top_customers ||
        data.top_customers.length === 0
    ) {

        const message =
            document.createElement("p");

        message.className =
            "analytics-loading";

        message.textContent =
            "No customer purchases available yet.";

        topCustomersBox.appendChild(
            message
        );

    } else {

        data.top_customers.forEach(
            function (customer, index) {

                const item =
                    document.createElement("div");

                item.className =
                    "analytics-item";


                const left =
                    document.createElement("div");


                const name =
                    document.createElement("div");

                name.className =
                    "analytics-name";

                name.textContent =
                    `${index + 1}. ${customer.customer_name}`;


                const details =
                    document.createElement("div");

                details.className =
                    "analytics-details";

                details.textContent =
                    `${customer.purchase_count} purchase${
                        customer.purchase_count === 1
                            ? ""
                            : "s"
                    }`;


                left.appendChild(name);

                left.appendChild(details);


                const right =
                    document.createElement("div");

                right.className =
                    "analytics-revenue";

                right.textContent =
                    formatCurrency(
                        customer.revenue
                    );


                item.appendChild(left);

                item.appendChild(right);


                topCustomersBox.appendChild(
                    item
                );
            }
        );
    }


} catch (error) {

    /*
     * Analytics failure must NEVER stop
     * the other buttons from working.
     */

    console.warn(
        "Analytics unavailable:",
        error
    );


    if (topProductsBox) {

        topProductsBox.innerHTML = `
            <p class="analytics-loading">
                Analytics unavailable.
            </p>
        `;
    }


    if (topCustomersBox) {

        topCustomersBox.innerHTML = `
            <p class="analytics-loading">
                Analytics unavailable.
            </p>
        `;
    }
}

}

// =========================
// Load Business Insights
// =========================

async function loadBusinessInsights() {

if (!insightsBox) {
    return;
}


try {

    const response =
        await fetch(
            `${API_URL}/businesses/${businessId}/insights`
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to load insights"
        );
    }


    insightsBox.innerHTML = "";


    if (
        !data.insights ||
        data.insights.length === 0
    ) {

        const emptyMessage =
            document.createElement("p");

        emptyMessage.className =
            "insight-item";

        emptyMessage.textContent =
            "No business insights are available yet.";


        insightsBox.appendChild(
            emptyMessage
        );

        return;
    }


    data.insights.forEach(
        function (insight) {

            const item =
                document.createElement("div");

            item.className =
                "insight-item";


            const icon =
                document.createElement("span");

            icon.className =
                "insight-icon";

            icon.textContent =
                "💡";


            const text =
                document.createElement("span");

            text.textContent =
                insight;


            item.appendChild(icon);

            item.appendChild(text);


            insightsBox.appendChild(
                item
            );
        }
    );


} catch (error) {

    console.warn(
        "Insights unavailable:",
        error
    );


    insightsBox.innerHTML = "";


    const errorMessage =
        document.createElement("p");

    errorMessage.className =
        "insight-item";

    errorMessage.textContent =
        "Unable to load business insights.";


    insightsBox.appendChild(
        errorMessage
    );
}

}

// =========================
// Create Business
// =========================

async function createBusiness() {

const name =
    businessNameInput.value.trim();

const industry =
    businessIndustryInput.value.trim();

const description =
    businessDescriptionInput.value.trim();


if (!name) {

    businessMessage.textContent =
        "Please enter a business name.";

    return;
}


if (!industry) {

    businessMessage.textContent =
        "Please enter an industry.";

    return;
}


createBusinessButton.disabled =
    true;

createBusinessButton.textContent =
    "Creating...";


businessMessage.textContent =
    "Creating business...";


try {

    const response =
        await fetch(
            `${API_URL}/businesses`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    name:
                        name,

                    industry:
                        industry,

                    description:
                        description
                })
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to create business"
        );
    }


    /*
     * Switch the application to the
     * newly created business.
     */

    businessId =
        data.id;


    businessMessage.textContent =
        `Business created successfully! ID: ${businessId}`;


    /*
     * Clear form
     */

    businessNameInput.value = "";

    businessIndustryInput.value = "";

    businessDescriptionInput.value = "";


    /*
     * Refresh dashboard for the
     * newly created business.
     */

    await refreshDashboard();


} catch (error) {

    console.error(
        "Create business error:",
        error
    );


    businessMessage.textContent =
        `Error: ${formatError(error)}`;


} finally {

    createBusinessButton.disabled =
        false;

    createBusinessButton.textContent =
        "Create Business";
}

}

// =========================
// Upload Button
// =========================
async function handleUploadClick() {

if (!businessFileInput) {
    return;
}

const file =
    businessFileInput.files[0];

if (!file) {

    if (uploadMessage) {
        uploadMessage.textContent =
            "Please select an Excel or CSV file first.";
    }

    return;
}

uploadButton.disabled = true;

uploadButton.textContent =
    "Uploading...";

if (uploadMessage) {
    uploadMessage.textContent =
        "Uploading and analyzing your business data...";
}

try {

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    /*
     * Your actual FastAPI endpoint is:
     *
     * POST /businesses/{business_id}/upload
     */

    const response =
        await fetch(
            `${API_URL}/businesses/${businessId}/upload`,
            {
                method: "POST",
                body: formData
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to upload business data."
        );
    }


    if (uploadMessage) {

        uploadMessage.textContent =
            data.message ||
            "Business data uploaded and analyzed successfully.";
    }


    /*
     * Clear selected file
     */

    businessFileInput.value = "";


    /*
     * Refresh dashboard after import
     */

    await refreshDashboard();


} catch (error) {

    console.error(
        "Upload error:",
        error
    );


    if (uploadMessage) {

        uploadMessage.textContent =
            `Upload failed: ${formatError(error)}`;
    }


} finally {

    uploadButton.disabled = false;

    uploadButton.textContent =
        "Upload & Analyze";
}

}


// =========================
// Add Customer
// =========================

async function addCustomer() {

const name =
    customerNameInput.value.trim();

const email =
    customerEmailInput.value.trim();


if (!name || !email) {

    customerMessage.textContent =
        "Please enter customer name and email.";

    return;
}


addCustomerButton.disabled =
    true;

addCustomerButton.textContent =
    "Adding...";


try {

    const response =
        await fetch(
            `${API_URL}/customers`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    business_id:
                        businessId,

                    name:
                        name,

                    email:
                        email
                })
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to add customer"
        );
    }


    customerMessage.textContent =
        "Customer added successfully.";


    customerNameInput.value = "";

    customerEmailInput.value = "";


    await refreshDashboard();


} catch (error) {

    console.error(
        "Add customer error:",
        error
    );


    customerMessage.textContent =
        formatError(error);


} finally {

    addCustomerButton.disabled =
        false;

    addCustomerButton.textContent =
        "Add Customer";
}


}

// =========================
// Add Product
// =========================

async function addProduct() {

const name =
    productNameInput.value.trim();

const price =
    Number(
        productPriceInput.value
    );


if (
    !name ||
    !price ||
    price <= 0
) {

    productMessage.textContent =
        "Please enter a valid product name and price.";

    return;
}


addProductButton.disabled =
    true;

addProductButton.textContent =
    "Adding...";


try {

    const response =
        await fetch(
            `${API_URL}/products`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    business_id:
                        businessId,

                    name:
                        name,

                    price:
                        price
                })
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to add product"
        );
    }


    productMessage.textContent =
        "Product added successfully.";


    productNameInput.value = "";

    productPriceInput.value = "";


    await refreshDashboard();


} catch (error) {

    console.error(
        "Add product error:",
        error
    );


    productMessage.textContent =
        formatError(error);


} finally {

    addProductButton.disabled =
        false;

    addProductButton.textContent =
        "Add Product";
}

}

// =========================
// Get Product Price
// =========================

async function getProductPrice(
productId
) {


const response =
    await fetch(
        `${API_URL}/products`
    );


const data =
    await response.json();


if (!response.ok) {

    throw new Error(
        data.detail ||
        "Unable to load products"
    );
}


const product =
    data.find(
        function (item) {

            return Number(item.id) ===
                Number(productId);
        }
    );


if (!product) {

    throw new Error(
        "Product not found."
    );
}


return Number(product.price);


}

// =========================
// Record Sale
// =========================

async function addSale() {

const productId =
    Number(
        saleProductIdInput.value
    );

const customerId =
    Number(
        saleCustomerIdInput.value
    );

const quantity =
    Number(
        saleQuantityInput.value
    );


if (
    !productId ||
    !customerId ||
    !quantity ||
    quantity <= 0
) {

    saleMessage.textContent =
        "Please enter valid product, customer, and quantity.";

    return;
}


addSaleButton.disabled =
    true;

addSaleButton.textContent =
    "Recording...";


try {

    const unitPrice =
        await getProductPrice(
            productId
        );


    const response =
        await fetch(
            `${API_URL}/sales`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    business_id:
                        businessId,

                    product_id:
                        productId,

                    customer_id:
                        customerId,

                    quantity:
                        quantity,

                    unit_price:
                        unitPrice
                })
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        let errorMessage =
            "Failed to record sale";


        if (
            Array.isArray(
                data.detail
            )
        ) {

            errorMessage =
                data.detail
                    .map(
                        function (error) {

                            return (
                                error.msg ||
                                "Invalid field"
                            );
                        }
                    )
                    .join(", ");

        } else if (
            data.detail
        ) {

            errorMessage =
                data.detail;

        } else if (
            data.error
        ) {

            errorMessage =
                data.error;
        }


        throw new Error(
            errorMessage
        );
    }


    saleMessage.textContent =
        `Sale recorded successfully. Total: ${formatCurrency(
            data.total_amount ??
            unitPrice * quantity
        )}`;


    saleProductIdInput.value =
        "";

    saleCustomerIdInput.value =
        "";

    saleQuantityInput.value =
        "1";


    await refreshDashboard();


} catch (error) {

    console.error(
        "Record sale error:",
        error
    );


    saleMessage.textContent =
        formatError(error);


} finally {

    addSaleButton.disabled =
        false;

    addSaleButton.textContent =
        "Record Sale";
}


}

// =========================
// Refresh Dashboard
// =========================

async function refreshDashboard() {

/*
 * Each section handles its own errors.
 * Therefore a failed analytics request
 * cannot stop the buttons.
 */

await loadBusinessMetrics();

await loadBusinessAnalytics();

await loadBusinessInsights();

}

// =========================
// Ask AI Assistant
// =========================

async function askAssistant() {

const question =
    questionInput.value.trim();


if (!question) {

    answerBox.textContent =
        "Please enter a question.";

    return;
}


askButton.disabled =
    true;

askButton.textContent =
    "Thinking...";


answerBox.textContent =
    "Getting your answer...";


try {

    const response =
        await fetch(
            `${API_URL}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    business_id:
                        businessId,

                    question:
                        question
                })
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to get answer"
        );
    }


    answerBox.textContent =
    (data.answer || "No answer was returned.")
        .replace(/\*\*/g, "")
        .replace(/\*/g, "");


} catch (error) {

    console.error(
        "Ask error:",
        error
    );


    answerBox.textContent =
        `Backend error: ${formatError(
            error
        )}`;


} finally {

    askButton.disabled =
        false;

    askButton.textContent =
        "Ask Assistant";
}

}

// =========================
// Event Listeners
// =========================

// Create Business

if (createBusinessButton) {

createBusinessButton.addEventListener(
    "click",
    createBusiness
);

}

// Upload

if (uploadButton) {

uploadButton.addEventListener(
    "click",
    handleUploadClick
);

}

// Customer

if (addCustomerButton) {


addCustomerButton.addEventListener(
    "click",
    addCustomer
);


}

// Product

if (addProductButton) {


addProductButton.addEventListener(
    "click",
    addProduct
);


}

// Sale

if (addSaleButton) {

addSaleButton.addEventListener(
    "click",
    addSale
);


}

// AI Assistant

if (askButton) {


askButton.addEventListener(
    "click",
    askAssistant
);

}

// =========================
// Enter Key For AI
// =========================

if (questionInput) {

questionInput.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            askAssistant();
        }
    }
);


}

// =========================
// Initial Page Load
// =========================

refreshDashboard().catch(
function (error) {

    console.error(
        "Dashboard startup error:",
        error
    );
}
);
