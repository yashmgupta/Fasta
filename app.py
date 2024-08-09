import streamlit as st
from Bio import SeqIO
import io
import csv

# Function to read and parse the FASTA file
def read_fasta(file):
    # Decode the file content and read it as a text stream
    fasta_sequences = list(SeqIO.parse(io.StringIO(file.getvalue().decode("utf-8")), "fasta"))
    return fasta_sequences

# Function to extract sequences based on identifiers
def extract_sequences(fasta_sequences, identifiers):
    return [seq for seq in fasta_sequences if seq.id in identifiers]

# Function to convert FASTA to CSV
def fasta_to_csv(fasta_sequences, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Sequence'])
        for record in fasta_sequences:
            writer.writerow([record.id, str(record.seq)])

# Function to filter sequences by length
def filter_by_length(fasta_sequences, min_length, max_length):
    return [seq for seq in fasta_sequences if min_length <= len(seq.seq) <= max_length]

# Main function for the Streamlit app
def main():
    st.title("FASTA File Manipulation for Scientific Studies")

    # Upload FASTA File
    fasta_file = st.file_uploader("Upload a FASTA file", type=["fasta", "fa"])

    if fasta_file is not None:
        # Read and parse the FASTA file
        fasta_sequences = read_fasta(fasta_file)
        
        # Option to extract sequences
        identifiers = st.text_area("Enter sequence IDs (comma-separated) to extract", "")
        if st.button("Extract Sequences"):
            id_list = [id.strip() for id in identifiers.split(",")]
            extracted_seqs = extract_sequences(fasta_sequences, id_list)
            st.write(f"Extracted {len(extracted_seqs)} sequences")
            st.download_button("Download Extracted Sequences", data=str(extracted_seqs), file_name="extracted_sequences.fasta")

        # Option to filter sequences by length
        min_length = st.number_input("Minimum sequence length", value=0)
        max_length = st.number_input("Maximum sequence length", value=1000)
        if st.button("Filter Sequences"):
            filtered_seqs = filter_by_length(fasta_sequences, min_length, max_length)
            st.write(f"Filtered to {len(filtered_seqs)} sequences")
            st.download_button("Download Filtered Sequences", data=str(filtered_seqs), file_name="filtered_sequences.fasta")

        # Option to convert FASTA to CSV
        if st.button("Convert to CSV"):
            output_csv = "sequences.csv"
            fasta_to_csv(fasta_sequences, output_csv)
            with open(output_csv, "rb") as file:
                st.download_button("Download CSV", file, file_name=output_csv)

if __name__ == "__main__":
    main()
