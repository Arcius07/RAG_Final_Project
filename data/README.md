# Knowledge Base Directory

This folder contains the PDF documents used for the RAG system.

## Setup Instructions

1. **Place your PDF here:**
   - Add your knowledge base PDF file as `knowledge_base.pdf`
   - The system expects the file path: `data/knowledge_base.pdf`

2. **PDF Requirements:**
   - Format: PDF (.pdf)
   - Content: Text-based (not scanned images)
   - Size: Recommended < 100MB (first ingestion will take longer with larger files)
   - Content: Customer support FAQs, policies, SOPs, etc.

3. **Example Structure for PDF:**
   ```
   FAQ Section:
   - How do I reset my password?
   - What's your shipping policy?
   - How do I process a refund?
   
   Policies:
   - Return Policy (30 days)
   - Privacy Policy
   - Terms of Service
   
   Troubleshooting:
   - Login Issues
   - Payment Problems
   - Account Recovery
   ```

4. **Test PDF (Optional):**
   If you don't have a PDF yet, create a sample document with:
   - Q: How do I reset my password?
     A: Go to login page > Click "Forgot Password" > Follow email link
   
   - Q: What's your return policy?
     A: Items can be returned within 30 days of purchase

5. **Ingestion Process:**
   Once you place the PDF here and run the app, it will:
   - Extract text from the PDF
   - Split into 500-token chunks (with 100-token overlap)
   - Generate embeddings using sentence-transformers
   - Store in ChromaDB for retrieval

6. **Updating the PDF:**
   - Replace `knowledge_base.pdf` with updated version
   - Delete the `../chroma_db/` folder
   - Restart the app (it will re-ingest automatically)

## Troubleshooting

**Error: "Place PDF at data/knowledge_base.pdf"**
- Solution: Ensure file exists at exact path with correct name

**Error: "PDF is scanned/image-based"**
- Solution: Use OCR or text-based PDF instead

**Empty search results**
- Solution: Verify PDF has relevant content related to queries
