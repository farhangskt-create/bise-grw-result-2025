import fitz  # PyMuPDF
import json

def generate_json_index(pdf_path, output_json_path):
    doc = fitz.open(pdf_path)
    records = []
    
    print("Reading gazette layout and recording row coordinates correctly...")
    for page_num in range(len(doc)):
        page = doc[page_num]
        words = page.get_text("words")
        if not words:
            continue
            
        page_width = page.rect.width
        mid_x = page_width / 2.0
        
        left_words = [w for w in words if w[0] < mid_x]
        right_words = [w for w in words if w[0] >= mid_x]
        
        # Define column bounds precisely based on actual layout margins
        columns = [
            (0, mid_x),          # Left column boundary
            (mid_x, page_width)  # Right column boundary
        ]
        
        for col_words in [left_words, right_words]:
            if not col_words:
                continue
                
            is_right_col = col_words[0][0] >= mid_x
            col_x0 = mid_x if is_right_col else 15  # left margin buffer
            col_x1 = page_width - 15 if is_right_col else mid_x - 5
                
            lines_dict = {}
            for w in col_words:
                y_coord = round(w[1], 1)
                matched_y = None
                for ey in lines_dict:
                    if abs(ey - y_coord) < 3.5:
                        matched_y = ey
                        break
                if matched_y is not None:
                    lines_dict[matched_y].append(w)
                else:
                    lines_dict[y_coord] = [w]
                    
            sorted_ys = sorted(lines_dict.keys())
            
            for i, y in enumerate(sorted_ys):
                row_words = sorted(lines_dict[y], key=lambda x: x[0])
                row_text = " ".join([w[4] for w in row_words]).strip()
                if not row_text:
                    continue
                
                parts = row_text.split()
                if len(parts) >= 1 and parts[0].isdigit() and len(parts[0]) == 6:
                    roll_num = parts[0]
                    name = " ".join(parts[1:])
                    
                    # Height box extending downwards to capture the full row data and marks block
                    next_y = y + 55
                    
                    records.append({
                        "roll_num": roll_num,
                        "name": name,
                        "page": page_num,
                        "bbox": [col_x0, y - 5, col_x1, next_y]
                    })

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4, ensure_ascii=False)
    
    print(f"Success! Generated '{output_json_path}' with {len(records)} records.")

if __name__ == "__main__":
    pdf_file = "gazette.pdf"
    generate_json_index(pdf_file, "gazette_index.json")