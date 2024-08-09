import streamlit as st
from Bio import SeqIO
import csv

def main():
    st.title("FASTA File Manipulation for Scientific Studies")

    # Upload FASTA File
    fasta_file = st.file_uploader("Upload a FASTA file", type=["fasta", "fa"])

    if fasta_file is not None:
        fasta_sequences = list(SeqIO.parse(fasta_file, "fasta"))
        
        # Extract Sequences
        identifiers = st.text_area("Enter sequence IDs (comma-separated) to extract", "")
        if st.button("Extract Sequences"):
            id_list = [id.strip() for id in identifiers.split(",")]
            extracted_seqs = extract_sequences(fasta_sequences, id_list)
            st.write(f"Extracted {len(extracted_seqs)} sequences")
            st.download_button("Download Extracted Sequences", data=str(extracted_seqs), file_name="extracted_sequences.fasta")

        # Filter by Length
        min_length = st.number_input("Minimum sequence length", value=0)
        max_length = st.number_input("Maximum sequence length", value=1000)
        if st.button("Filter Sequences"):
            filtered_seqs = filter_by_length(fasta_sequences, min_length, max_length)
            st.write(f"Filtered to {len(filtered_seqs)} sequences")
            st.download_button("Download Filtered Sequences", data=str(filtered_seqs), file_name="filtered_sequences.fasta")

        # Convert to CSV
        if st.button("Convert to CSV"):
            output_csv = "sequences.csv"
            fasta_to_csv(fasta_sequences, output_csv)
            with open(output_csv, "rb") as file:
                st.download_button("Download CSV", file, file_name=output_csv)

if __name__ == "__main__":
    main()
