import asyncio
import os
import json
import argparse
from llama_extract import LlamaExtract
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
extractor = LlamaExtract()

async def batch_process_termsheets(directory, output_dir=None):
    """Process all PDFs in a directory and save results"""
    if output_dir is None:
        output_dir = os.path.join(directory, 'extracted_data')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Use existing agent for Structured Product Termsheet
    agent = extractor.get_agent(id="50297c9a-d871-4218-90b7-79548adbd6ce")
    
    # Get all PDF files in the directory
    pdf_files = [os.path.join(directory, f) for f in os.listdir(directory) 
                if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {directory}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Queue all files for extraction
    jobs = await agent.queue_extraction(pdf_files)
    
    # Track job status
    completed = 0
    print(f"Queued {len(jobs)} extraction jobs")
    
    while completed < len(jobs):
        completed = 0
        for job in jobs:
            job_status = agent.get_extraction_job(job.id).status
            if job_status == 'completed':
                completed += 1
            elif job_status == 'failed':
                print(f"Job {job.id} failed")
                completed += 1
        
        if completed < len(jobs):
            print(f"Progress: {completed}/{len(jobs)} completed")
            await asyncio.sleep(3)
    
    print("All jobs completed!")
    
    # Get and save results
    for i, job in enumerate(jobs):
        try:
            result = agent.get_extraction_run_for_job(job.id)
            if result:
                # Get original filename without extension
                original_filename = os.path.basename(pdf_files[i])
                base_filename = os.path.splitext(original_filename)[0]
                
                # Save results as JSON
                output_path = os.path.join(output_dir, f"{base_filename}.json")
                with open(output_path, 'w') as f:
                    json.dump(result.data, f, indent=2, default=str)
                
                print(f"Saved results for {original_filename} to {output_path}")
            else:
                print(f"No results for job {job.id}")
        except Exception as e:
            print(f"Error retrieving results for job {job.id}: {e}")
    
    return output_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch process termsheets")
    parser.add_argument("directory", help="Directory containing PDF termsheets")
    parser.add_argument("--output", help="Output directory for extracted data")
    args = parser.parse_args()
    
    asyncio.run(batch_process_termsheets(args.directory, args.output)) 