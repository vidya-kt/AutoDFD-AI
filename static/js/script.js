// Initialize Mermaid
mermaid.initialize({

    startOnLoad: false,

    theme: "default",

    securityLevel: "loose"
});

let detectedLevel = "";

// DOM Elements
const generateBtn = document.getElementById("generateBtn");

const clearBtn = document.getElementById("clearBtn");

const copyBtn = document.getElementById("copyBtn");

const pngBtn = document.getElementById("pngBtn");

const pdfBtn = document.getElementById("pdfBtn");

const descriptionInput = document.getElementById("description");

const diagramDiv = document.getElementById("diagram");

const mermaidCodeBlock = document.getElementById("mermaidCode");

const loadingContainer = document.getElementById("loading");

const charCount = document.getElementById("charCount");


// Character Counter
descriptionInput.addEventListener("input", () => {

    charCount.textContent = descriptionInput.value.length;
});


// Generate DFD
generateBtn.addEventListener("click", async () => {

    const description = descriptionInput.value.trim();

    // Validation
    if(description === ""){

        showToast("Please enter system description", "danger");

        return;
    }

    // Show loading
    showLoading(true);

    try{

        const response = await fetch("/generate-dfd", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                description: description
            })
        });

        const data = await response.json();

        // Hide loading
        showLoading(false);

        // Error handling
        if(!data.success){

            showToast(data.error, "danger");

            return;
        }

        const mermaidCode = data.mermaid;

        detectedLevel = data.level;

        const levelBadge =
            document.getElementById("dfdLevelBadge");

        levelBadge.style.display = "inline-block";

        const levelNames = {

            "LEVEL_0": "Level 0 - Context Diagram",

            "LEVEL_1": "Level 1 - Major Process DFD",

            "LEVEL_2": "Level 2 - Detailed Process DFD"
        };

        levelBadge.textContent =
            "Detected: " +
            (levelNames[detectedLevel] || detectedLevel);

        // Display Mermaid code
        mermaidCodeBlock.textContent = mermaidCode;

        // Render Diagram
        renderMermaidDiagram(mermaidCode);

        // Scroll to output
        document
            .getElementById("diagramContainer")
            .scrollIntoView({
                behavior: "smooth"
            });

        showToast("DFD Generated Successfully", "success");

    }

    catch(error){

        showLoading(false);

        showToast(
            "Something went wrong",
            "danger"
        );

        console.error(error);
    }
});


// Render Mermaid Diagram
async function renderMermaidDiagram(code){

    try{

        // Clean code
        code = code
            .replace(/```mermaid/g, "")
            .replace(/```/g, "")
            .trim();

        // Clear old diagram
        diagramDiv.innerHTML = "";

        // Unique ID
        const uniqueId =
            "mermaid-" + Date.now();

        // Render Mermaid
        const renderResult =
            await mermaid.render(
                uniqueId,
                code
            );

        // Insert SVG
        diagramDiv.innerHTML =
            renderResult.svg;

    }

    catch(error){

        console.error(error);

        diagramDiv.innerHTML = `

            <div class="alert alert-danger">

                Invalid Mermaid Syntax Generated

            </div>
        `;
    }
}


// Clear Button
clearBtn.addEventListener("click", () => {

    descriptionInput.value = "";

    mermaidCodeBlock.textContent = "";

    diagramDiv.innerHTML = `

        <p class="placeholder-text">

            Your generated DFD diagram will appear here.

        </p>
    `;

    charCount.textContent = "0";

    showToast("Cleared Successfully", "warning");
});


// Copy Mermaid Code
copyBtn.addEventListener("click", async () => {

    const code = mermaidCodeBlock.textContent;

    if(code.trim() === ""){

        showToast("No Mermaid code available", "danger");

        return;
    }

    try{

        await navigator.clipboard.writeText(code);

        showToast("Code Copied", "success");
    }

    catch(error){

        showToast("Copy Failed", "danger");
    }
});


// Export PNG
pngBtn.addEventListener("click", async () => {

    try{

        const exportContainer =
            document.createElement("div");

        exportContainer.style.padding = "30px";
        exportContainer.style.background = "white";
        exportContainer.style.color = "black";

        // Title
        exportContainer.innerHTML = `

            <h1 style="text-align:center;
                       margin-bottom:10px;">

                AutoDFD AI

            </h1>

            <h3 style="text-align:center;
                       margin-bottom:20px;">

                Generated Data Flow Diagram

            </h3>

            <p style="text-align:center;
                      font-size:18px;
                      font-weight:bold;
                      margin-bottom:20px;">

               Detected DFD Level:
               ${detectedLevel}

            </p>

            <p style="margin-bottom:20px;">
                <strong>Description:</strong>
                ${descriptionInput.value}
            </p>
        `;

        // Clone diagram
        const diagramClone =
            diagramDiv.cloneNode(true);

        exportContainer.appendChild(diagramClone);

        document.body.appendChild(exportContainer);

        const canvas =
            await html2canvas(exportContainer);

        const image =
            canvas.toDataURL("image/png");

        const link =
            document.createElement("a");

        link.href = image;

        link.download = "AutoDFD_AI-Diagram.png";

        link.click();

        document.body.removeChild(exportContainer);

        showToast(
            "PNG Downloaded",
            "success"
        );

    }

    catch(error){

        console.error(error);

        showToast(
            "PNG Export Failed",
            "danger"
        );
    }
});


// Export PDF
pdfBtn.addEventListener("click", async () => {

    try{

        const exportContainer =
            document.createElement("div");

        exportContainer.style.padding = "30px";
        exportContainer.style.background = "white";
        exportContainer.style.color = "black";
        exportContainer.style.width = "1000px";

        exportContainer.innerHTML = `

            <h1 style="text-align:center;
                       margin-bottom:10px;">

                AutoDFD AI

            </h1>

            <h3 style="text-align:center;
                       margin-bottom:20px;">

                Generated Data Flow Diagram

            </h3>

            <p style="text-align:center;
                      font-size:18px;
                      font-weight:bold;
                      margin-bottom:20px;">

               Detected DFD Level:
               ${detectedLevel}

            </p>

            <p style="margin-bottom:20px;">
                <strong>Description:</strong>
                ${descriptionInput.value}
            </p>
        `;

        // Clone diagram
        const diagramClone =
            diagramDiv.cloneNode(true);

        exportContainer.appendChild(diagramClone);

        document.body.appendChild(exportContainer);

        const canvas =
            await html2canvas(exportContainer);

        const image =
            canvas.toDataURL("image/png");

        const { jsPDF } = window.jspdf;

        const pdf = new jsPDF(
            "p",
            "mm",
            "a4"
        );

        const imgWidth = 190;

        const pageHeight = 295;

        const imgHeight =
            canvas.height * imgWidth / canvas.width;

        let heightLeft = imgHeight;

        let position = 10;

        pdf.setFontSize(18);

        pdf.setFontSize(18);

    pdf.text(
        "AutoDFD AI Report",
        pdf.internal.pageSize.getWidth() / 2,
        10,
        { align: "center" }
    );

        pdf.addImage(
            image,
            "PNG",
            10,
            20,
            imgWidth,
            imgHeight
        );

        heightLeft -= pageHeight;

        while(heightLeft >= 0){

            position = heightLeft - imgHeight;

            pdf.addPage();

            pdf.addImage(
                image,
                "PNG",
                10,
                position,
                imgWidth,
                imgHeight
            );

            heightLeft -= pageHeight;
        }

        pdf.save(
            "DFDGenAI-Report.pdf"
        );

        document.body.removeChild(exportContainer);

        showToast(
            "PDF Downloaded",
            "success"
        );

    }

    catch(error){

        console.error(error);

        showToast(
            "PDF Export Failed",
            "danger"
        );
    }
});


// Loading State
function showLoading(show){

    if(show){

        loadingContainer.classList.remove("d-none");
    }

    else{

        loadingContainer.classList.add("d-none");
    }
}


// Toast Notification
function showToast(message, type){

    // Remove existing toast
    const oldToast =
        document.querySelector(".custom-toast");

    if(oldToast){

        oldToast.remove();
    }

    // Create toast
    const toast = document.createElement("div");

    toast.className =
        `alert alert-${type} custom-toast`;

    toast.innerHTML = `
        ${message}
    `;

    document.body.appendChild(toast);

    // Remove after 3 sec
    setTimeout(() => {

        toast.remove();

    }, 3000);
}

// Scroll Animation
window.addEventListener("scroll", () => {

    const navbar =
        document.querySelector(".custom-navbar");

    if(window.scrollY > 50){

        navbar.style.background =
            "rgba(0,0,0,0.6)";
    }

    else{

        navbar.style.background =
            "rgba(0,0,0,0.3)";
    }
});