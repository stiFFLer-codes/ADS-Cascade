const fs = require('fs');
const path = require('path');

const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D406 Invoice Classification — Phase 1 Comprehensive Review</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f9f9f9;
        }
        .container {
            background-color: #fff;
            padding: 3rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
            font-size: 2.2rem;
        }
        h2 {
            color: #2980b9;
            margin-top: 3.5rem;
            border-bottom: 1px solid #eee;
            padding-bottom: 0.5rem;
            font-size: 1.8rem;
        }
        h3 {
            color: #34495e;
            margin-top: 2.5rem;
            font-size: 1.4rem;
        }
        .status-block {
            background-color: #e8f4f8;
            border-left: 4px solid #3498db;
            padding: 1.5rem;
            margin-bottom: 2.5rem;
            border-radius: 0 4px 4px 0;
            font-size: 1.1rem;
        }
        .status-block p {
            margin: 0.5rem 0;
            font-weight: 500;
        }
        .hero-statement {
            font-size: 1.3rem;
            color: #2c3e50;
            font-weight: 600;
            margin: 2rem 0;
            padding: 1.5rem;
            background-color: #f4f6f7;
            border-radius: 6px;
            text-align: center;
        }
        .impact-box {
            display: flex;
            justify-content: space-between;
            gap: 2rem;
            margin: 2rem 0;
        }
        .impact-card {
            flex: 1;
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 6px;
            border: 1px solid #e9ecef;
            text-align: center;
        }
        .impact-card h4 {
            font-size: 2rem;
            color: #e74c3c;
            margin: 0 0 0.5rem 0;
        }
        .impact-card p {
            font-size: 1.1rem;
            color: #555;
            margin: 0;
            font-weight: 500;
        }
        .before-after {
            display: flex;
            gap: 2rem;
            margin: 1.5rem 0;
        }
        .before-after > div {
            flex: 1;
            padding: 1.5rem;
            border-radius: 6px;
            text-align: center;
            font-weight: 600;
            font-size: 1.1rem;
        }
        .before-box {
            background-color: #fdedec;
            border: 1px solid #fadbd8;
            color: #c0392b;
        }
        .after-box {
            background-color: #eafaf1;
            border: 1px solid #d5f5e3;
            color: #27ae60;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 0.95rem;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background-color: #f4f6f7;
            color: #2c3e50;
            font-weight: 600;
        }
        .snapshot-box {
            background-color: #fafbfc;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            overflow-x: auto;
        }
        .snapshot-box h4 {
            margin-top: 0;
            color: #24292e;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.5rem;
        }
        .deliverables-box {
            background-color: #f1f8ff;
            border-left: 4px solid #0366d6;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0 4px 4px 0;
        }
        .deliverables-box h4 {
            margin-top: 0;
            color: #0366d6;
            margin-bottom: 0.5rem;
        }
        .deliverables-box ul {
            margin: 0;
            padding-left: 1.2rem;
        }
        .deliverables-box code {
            background-color: #e1efff;
            padding: 2px 6px;
            border-radius: 3px;
            color: #005cc5;
        }
        .why-matters-box {
            background-color: #fdf2e9;
            border-left: 4px solid #e67e22;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0 4px 4px 0;
        }
        .why-matters-box h4 {
            margin-top: 0;
            color: #d35400;
            margin-bottom: 0.5rem;
        }
        .why-matters-box p {
            margin: 0;
            font-size: 1.1rem;
            color: #4a2311;
        }
        .mermaid {
            background-color: #fcfcfc;
            border: 1px solid #eee;
            padding: 1.5rem;
            border-radius: 4px;
            text-align: center;
            margin: 2rem 0;
        }
        .evolution-path {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #fff;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.05);
            margin: 2rem 0;
            flex-wrap: wrap;
        }
        .evolution-step {
            text-align: center;
            position: relative;
        }
        .evolution-step h5 {
            margin: 0 0 0.5rem 0;
            color: #3498db;
            font-size: 1.1rem;
        }
        .evolution-step p {
            margin: 0;
            font-weight: bold;
            font-size: 1.2rem;
            color: #2c3e50;
        }
        .arrow {
            color: #bdc3c7;
            font-size: 1.5rem;
            font-weight: bold;
        }
        .note {
            background-color: #e8f4f8;
            border-left: 4px solid #3498db;
            padding: 1rem;
            margin: 1.5rem 0;
            font-size: 1.1rem;
            font-style: italic;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true});</script>
</head>
<body>
    <div class="container">
        <h1>D406 Invoice Classification — Phase 1 Review</h1>
        
        <div class="status-block">
            <p><strong>Status:</strong> Phase 1 Complete</p>
            <p><strong>Objective:</strong> Transform raw D406 fiscal data into an evidence-driven AI architecture.</p>
        </div>

        <h2>Why Phase 1 Exists</h2>
        <p class="hero-statement">
            The objective of Phase 1 was <strong>not</strong> to build an AI model.<br>
            The objective was to understand the data well enough that the AI architecture could be chosen based on <strong>evidence rather than assumptions</strong>.
        </p>
        <p>Why did we spend time building six scripts instead of immediately building an AI? Because building AI without understanding the data is guessing. By carefully extracting, measuring, and analyzing the fiscal declarations first, we engineered a solution that is significantly cheaper, faster, and more accurate.</p>

        <h2>Phase 1 Evolution</h2>
        <p>This single view tells the entire story of the project. We didn't just move data around; we refined chaos into intelligence.</p>
        <div class="evolution-path">
            <div class="evolution-step">
                <h5>Raw Files</h5>
                <p>1,290</p>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Normalized XML</h5>
                <p>1,020</p>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>GL Accounts</h5>
                <p>154,068</p>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Invoice Lines</h5>
                <p>296,648</p>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Knowledge Base</h5>
                <p>55,394 Products</p>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Architecture</h5>
                <p>Hybrid</p>
            </div>
        </div>

        <hr style="border: 0; height: 1px; background: #eee; margin: 3rem 0;">

        <h2>Script-by-Script Walkthrough</h2>

        <!-- SCRIPT 1 -->
        <h3>Script 1 & 1.5: Inventory & Normalization</h3>
        <p><strong>Objective:</strong> Parse the dataset manifest and standardize the environment before any analysis begins.</p>
        <p><strong>Process:</strong> Downloads ➡️ ZIP ➡️ Extraction ➡️ XML Validation ➡️ Normalized Repository</p>

        <div class="before-after">
            <div class="before-box">Before<br><br>Scattered ZIPs, network errors, and disparate XML schemas</div>
            <div class="after-box">After<br><br>A normalized, schema-validated repository of 201 companies ready for ML extraction</div>
        </div>

        <div class="snapshot-box">
            <h4>Output Snapshot: <code>companies_inventory.csv</code></h4>
            <table>
                <thead>
                    <tr><th>CUI</th><th>Company Name</th><th>CAEN Code</th><th>XML File Count</th></tr>
                </thead>
                <tbody>
                    <tr><td>12345678</td><td>ABC SRL</td><td>4711</td><td>12</td></tr>
                    <tr><td>87654321</td><td>XYZ INC</td><td>6201</td><td>24</td></tr>
                </tbody>
            </table>
        </div>

        <div class="deliverables-box">
            <h4>Files Produced</h4>
            <ul>
                <li><code>companies_inventory.csv</code></li>
                <li><code>data/normalized/*.xml</code></li>
            </ul>
        </div>

        <div class="why-matters-box">
            <h4>Business Value</h4>
            <p>Normalization ensures that every downstream script interacts with standard, schema-validated D406 XMLs. We avoid repeating fragile download/extraction logic, creating a clean foundation for the entire pipeline.</p>
        </div>


        <!-- SCRIPT 2 -->
        <h3>Script 2: Teaching the System Accounting</h3>
        <p><strong>Objective:</strong> Extract the Chart of Accounts from each company to provide accounting context.</p>
        <p><strong>Process:</strong> Normalized XML ➡️ General Ledger Accounts ➡️ GL Knowledge Base</p>

        <div class="before-after">
            <div class="before-box">Before Script 2<br><br>The XML simply says:<br>AccountID: 707<br><em>(That number means nothing to an AI)</em></div>
            <div class="after-box">After Script 2<br><br>707 = Revenue from Goods = Revenue Account<br><em>(Now the AI understands accounting)</em></div>
        </div>

        <div class="snapshot-box">
            <h4>Output Snapshot: <code>company_gl_accounts.csv</code></h4>
            <table>
                <thead>
                    <tr><th>CUI</th><th>AccountID</th><th>Description</th><th>Type</th></tr>
                </thead>
                <tbody>
                    <tr><td>12345</td><td>707</td><td>Revenue Goods</td><td>Asset</td></tr>
                    <tr><td>12345</td><td>704</td><td>Revenue Services</td><td>Asset</td></tr>
                    <tr><td>12345</td><td>371</td><td>Inventory</td><td>Liability</td></tr>
                </tbody>
            </table>
        </div>

        <div class="deliverables-box">
            <h4>Files Produced</h4>
            <ul>
                <li><code>company_gl_accounts.csv</code></li>
                <li><code>company_gl_catalog.json</code></li>
                <li><code>gl_statistics.csv</code></li>
            </ul>
        </div>

        <div class="why-matters-box">
            <h4>Business Value</h4>
            <p>This dataset becomes the accounting dictionary for every company. Without it, the AI would only see numerical AccountIDs without understanding their meaning.</p>
        </div>


        <!-- SCRIPT 3 -->
        <h3>Script 3: Learning From Real Accountant Decisions</h3>
        <p><strong>Objective:</strong> Extract granular transaction data from complex XMLs to build our ground-truth AI training set.</p>
        <p><strong>Process:</strong> Invoice ➡️ Invoice Lines ➡️ Enrichment ➡️ Knowledge Base ➡️ CSV</p>

        <div class="before-after">
            <div class="before-box">Before Script 3<br><br>Invoices</div>
            <div class="after-box">After Script 3<br><br>296,648 Accounting Decisions</div>
        </div>

        <div class="snapshot-box">
            <h4>Output Snapshot: <code>invoice_lines_all_companies.csv</code></h4>
            <table>
                <thead>
                    <tr><th>Company</th><th>Invoice</th><th>Product</th><th>VAT</th><th>AccountID</th></tr>
                </thead>
                <tbody>
                    <tr><td>ABC SRL</td><td>INV-101</td><td>Dell Laptop</td><td>19%</td><td>707</td></tr>
                    <tr><td>ABC SRL</td><td>INV-102</td><td>Consulting Services</td><td>19%</td><td>704</td></tr>
                    <tr><td>XYZ INC</td><td>INV-205</td><td>Office Supplies</td><td>19%</td><td>302</td></tr>
                </tbody>
            </table>
        </div>

        <div class="deliverables-box">
            <h4>Files Produced</h4>
            <ul>
                <li><code>invoice_lines_all_companies.csv</code></li>
                <li><code>product_account_mapping.csv</code></li>
            </ul>
        </div>

        <div class="why-matters-box">
            <h4>Business Value</h4>
            <p>This is the ground-truth dataset. Every row represents a real accounting decision made by a human accountant. This dataset will eventually teach the AI how invoices are classified.</p>
        </div>


        <!-- SCRIPT 3.5 -->
        <h3>Script 3.5: Measuring the Difficulty Before Building AI</h3>
        <p><strong>Objective:</strong> Statistically measure the inherent difficulty of the dataset before designing the architecture.</p>
        <p><strong>Process:</strong> Raw Data ➡️ Quality Check ➡️ Determinism Scoring ➡️ Intelligence Metrics</p>
        
        <p>Originally, we planned to go straight from data extraction (Script 3) to architecture (Script 4). But building AI without understanding the data would be guessing. So we inserted Script 3.5. This single design decision transformed the project from <em>"AI development"</em> into <em>"Evidence-driven AI engineering."</em></p>

        <div class="impact-box">
            <div class="impact-card">
                <h4>74.5%</h4>
                <p>Global Determinism (Low consistency across different companies)</p>
            </div>
            <div class="impact-card">
                <h4>97.2%</h4>
                <p>Company Determinism (High consistency within the same company)</p>
            </div>
        </div>

        <div class="snapshot-box">
            <h4>Output Snapshot: Intelligence Metrics</h4>
            <table>
                <thead>
                    <tr><th>Metric</th><th>Value</th><th>Observation</th></tr>
                </thead>
                <tbody>
                    <tr><td><strong>ADS (Overall)</strong></td><td>0.847</td><td>Good, but not perfect globally</td></tr>
                    <tr><td><strong>Company ADS</strong></td><td>0.972</td><td>Highly deterministic internally</td></tr>
                    <tr><td><strong>VAT Stability</strong></td><td>94.46%</td><td>Very strong secondary feature</td></tr>
                </tbody>
            </table>
        </div>

        <div class="deliverables-box">
            <h4>Files Produced</h4>
            <ul>
                <li><code>dataset_intelligence.csv</code></li>
                <li><code>cross_company_consistency.csv</code></li>
                <li><code>vat_stability.csv</code></li>
            </ul>
        </div>

        <div class="why-matters-box">
            <h4>Business Value</h4>
            <p>These metrics allowed us to choose the AI architecture using evidence rather than assumptions. The massive gap between global and company determinism proved that simply knowing which company issued the invoice increases classification consistency dramatically.</p>
        </div>


        <!-- SCRIPT 4 -->
        <h3>Script 4: Architecture Decision</h3>
        <p><strong>Objective:</strong> Use the intelligence metrics to power an objective decision engine for Phase 2.</p>
        <p><strong>Process:</strong> Metrics ➡️ Decision Engine Rules ➡️ Final Architecture</p>

        <div class="before-after">
            <div class="before-box">Original Assumption<br><br>One Global Model</div>
            <div class="after-box">Dataset Says<br><br>Companies behave differently</div>
        </div>

        <div class="snapshot-box">
            <h4>Output Snapshot: Decision Engine Table</h4>
            <table>
                <thead>
                    <tr><th>Metric</th><th>Observation</th><th>Decision</th></tr>
                </thead>
                <tbody>
                    <tr><td><strong>ADS</strong></td><td>0.847</td><td><span class="highlight">Hybrid Retrieval</span></td></tr>
                    <tr><td><strong>Company Determinism</strong></td><td>0.972</td><td><span class="highlight">Company Knowledge Base</span></td></tr>
                    <tr><td><strong>Warehouse ID</strong></td><td>100% missing</td><td><span class="highlight">Remove Feature</span></td></tr>
                    <tr><td><strong>VAT</strong></td><td>94.46% stable</td><td><span class="highlight">Secondary Feature</span></td></tr>
                </tbody>
            </table>
        </div>

        <div class="deliverables-box">
            <h4>Files Produced</h4>
            <ul>
                <li><code>architecture_decision.md</code></li>
                <li><code>decision_matrix.csv</code></li>
            </ul>
        </div>

        <div class="why-matters-box">
            <h4>Business Value</h4>
            <p>This proves that the final architecture is not a guess. Instead of forcing an expensive LLM to predict everything, we handle 91% of the data with a cheap, 100% accurate rule lookup tied to company-specific Knowledge Bases, and only use embeddings for the ambiguous tail.</p>
        </div>

        <hr style="border: 0; height: 1px; background: #eee; margin: 3rem 0;">

        <h2>How Everything Worked Together</h2>
        <div class="mermaid">
        flowchart LR
            Client --> Manifest["JSON Manifest"]
            Manifest --> S1["Script 1<br>Company Inventory"]
            S1 --> S15["Script 1.5<br>Normalize XML"]
            S15 --> S2["Script 2<br>Understand Accounting"]
            S2 --> S3["Script 3<br>Extract Human Decisions"]
            S3 --> S35["Script 3.5<br>Understand Dataset Behavior"]
            S35 --> S4["Script 4<br>Choose Best AI Architecture"]
            S4 --> P2["Phase 2<br>Build AI"]
        </div>

        <div class="evolution-path" style="margin-top: 1rem;">
            <div class="evolution-step">
                <h5>Raw Files</h5>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Structured Data</h5>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Accounting Knowledge</h5>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Business Intelligence</h5>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Architecture</h5>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>AI</h5>
            </div>
        </div>

        <h2>What Phase 1 Achieved</h2>
        <table>
            <thead>
                <tr>
                    <th>Deliverable</th>
                    <th>Purpose</th>
                    <th>Business Question Answered</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Company Inventory</strong></td>
                    <td>Identifies every company and its declarations</td>
                    <td>What companies are present?</td>
                </tr>
                <tr>
                    <td><strong>Normalized XML Repository</strong></td>
                    <td>Single clean source for all processing</td>
                    <td>Is our data clean and reusable?</td>
                </tr>
                <tr>
                    <td><strong>GL Knowledge Base</strong></td>
                    <td>Explains accounting meanings of AccountIDs</td>
                    <td>What does each AccountID mean?</td>
                </tr>
                <tr>
                    <td><strong>Transaction Dataset</strong></td>
                    <td>Ground-truth accounting decisions</td>
                    <td>How do accountants classify invoices?</td>
                </tr>
                <tr>
                    <td><strong>Product Knowledge Base</strong></td>
                    <td>Product ➡️ Account mappings</td>
                    <td>Which products map to which accounts?</td>
                </tr>
                <tr>
                    <td><strong>Dataset Intelligence</strong></td>
                    <td>Measures quality and determinism</td>
                    <td>How difficult is this problem?</td>
                </tr>
                <tr>
                    <td><strong>Architecture Recommendation</strong></td>
                    <td>Defines Phase 2 implementation</td>
                    <td>What should we build?</td>
                </tr>
            </tbody>
        </table>

        <h2>Phase 2 Starts Here</h2>
        <div class="evolution-path">
            <div class="evolution-step">
                <h5>Phase 1</h5>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Evidence</h5>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Company Knowledge Bases</h5>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Hybrid Retrieval</h5>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>AI Classification</h5>
            </div>
            <div class="arrow">➔</div>
            <div class="evolution-step">
                <h5>Accounting Automation</h5>
            </div>
        </div>

        <p>Phase 1 intentionally stopped before building AI. The objective was to eliminate assumptions and allow the data itself to determine the architecture. With the completion of this phase, the project now has the datasets, knowledge bases, quality metrics, and architectural guidance required to begin implementing an evidence-driven invoice classification system.</p>

        <div class="status-block" style="text-align: center; font-size: 1.5rem; border-left: none; background-color: #2ecc71; color: white;">
            <strong>Phase 1 Completed</strong>
        </div>

    </div>
</body>
</html>`;

const outputPath = path.join(__dirname, 'phase1_presentation_document.html');
fs.writeFileSync(outputPath, htmlContent);
console.log('Document successfully generated at:', outputPath);
