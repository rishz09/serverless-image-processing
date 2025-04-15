import streamlit as st
from backend import process_uploaded_images_sketch  # Ensure this import is correct
from backend import process_uploaded_images_bg_remove, process_uploaded_images_caption
# ---------- Page Config ----------
st.set_page_config(page_title="Serverless Image Processing", layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    .left-box {
        background: linear-gradient(135deg, #0047AB, #007BFF);
        color: white;
        border-radius: 15px;
        padding: 2.5rem;
        height: 85vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .title-text {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
    }
    .stButton > button#home-button {
        background-color: #007BFF;
        color: white;
        font-size: 18px;
        padding: 1rem 2rem;
        border-radius: 8px;
        width: auto;
        box-shadow: 0 4px 6px rgba(0, 123, 255, 0.3);
        margin-top: 2rem;
    }
    .stButton > button#home-button:hover {
        background-color: #0056b3;
        transform: scale(1.05);
    }
    .custom-title h2, .custom-title h3 {
        color: #0047AB;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .op-box, .upload-box, .result-box {
        background-color: #f1f3f5;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_operation" not in st.session_state:
    st.session_state.selected_operation = None
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

# ---------- Navigation Functions ----------
def go_to(operation=None):
    if operation:
        st.session_state.selected_operation = operation
    if st.session_state.page == "home":
        st.session_state.page = "operation"
    elif st.session_state.page == "operation":
        st.session_state.page = "upload"
    elif st.session_state.page == "upload":
        st.session_state.page = "result"

def go_back():
    if st.session_state.page == "upload":
        st.session_state.page = "operation"
    elif st.session_state.page == "operation":
        st.session_state.page = "home"

# ---------- Page 1: Homepage ----------
if st.session_state.page == "home":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
            <div class="left-box">
                <div class="title-text">Serverless<br>Image Processing</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <h3>Welcome 👋</h3>
            <p>
                This application demonstrates the use of <b>Serverless Computing</b> for intelligent image processing.<br><br>
                Users can choose from the following operations:
                <ul>
                    <li>🎨 Convert an image to a sketch</li>
                    <li>🧼 Remove background from any image</li>
                    <li>🧠 Generate AI-based image captions</li>
                </ul>
                <br>
                This system supports <b>multiple concurrent users</b> and uses <b>load balancing and auto-scaling</b> techniques on Google Cloud.
            </p>
        """, unsafe_allow_html=True)
        if st.button("🚀 Get Started", key="home-button"):
            go_to()

# ---------- Page 2: Operation Selection ----------
elif st.session_state.page == "operation":
    st.markdown("<div class='custom-title'><h3>Choose Functionality</h3></div>", unsafe_allow_html=True)
    st.markdown("<h3>Select an Operation</h3>", unsafe_allow_html=True)
    st.markdown("<p>Choose one of the following image processing tasks:</p>", unsafe_allow_html=True)
    st.button("🎨 Image to Sketch", on_click=lambda: go_to("sketch"), key="btn-sketch", help="Convert an image into a sketch")
    st.button("🧼 Background Removal", on_click=lambda: go_to("bg_remove"), key="btn-bg-remove", help="Remove background (Coming soon)")
    st.button("🧠 Image Captioning", on_click=lambda: go_to("caption"), key="btn-caption", help="Generate captions (Coming soon)")
    st.markdown("---")
    st.button("⬅️ Back", on_click=go_back)

# ---------- Page 3: Upload ----------
elif st.session_state.page == "upload":
    op_title = {
        "sketch": "🎨 Image to Sketch",
        "bg_remove": "🧼 Background Removal",
        "caption": "🧠 Image Captioning"
    }.get(st.session_state.selected_operation, "Operation")
    st.markdown(f"<div class='custom-title'><h3>{op_title}</h3></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; margin-bottom: 2rem;">
        <p style="font-size: 2rem; line-height: 1.8; color: #333;">Upload one or more images below:</p>
    </div>
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("⚙️ Process Images", on_click=go_to)
    st.markdown("---")
    st.button("⬅️ Back", on_click=go_back)
    
# ---------- Page 4: Result ----------
elif st.session_state.page == "result":
    st.markdown("<div class='custom-title'><h3>✅ Output</h3></div>", unsafe_allow_html=True)
    
    # Process images only if not already done
    if st.session_state.selected_operation == "sketch" and st.session_state.uploaded_files and not st.session_state.processed_files:
        processed_files = process_uploaded_images_sketch(st.session_state.selected_operation,
                                                  st.session_state.uploaded_files)
        st.session_state.processed_files = processed_files
    
    if st.session_state.selected_operation == "bg_remove" and st.session_state.uploaded_files and not st.session_state.processed_files:
        processed_files = process_uploaded_images_bg_remove(st.session_state.selected_operation,
                                                  st.session_state.uploaded_files)
        st.session_state.processed_files = processed_files
    
    if st.session_state.selected_operation == "caption" and st.session_state.uploaded_files and not st.session_state.processed_files:
        processed_files = process_uploaded_images_caption(st.session_state.selected_operation,
                                                  st.session_state.uploaded_files)
        st.session_state.processed_files = processed_files

    if not st.session_state.uploaded_files:
        st.warning("No images uploaded. Please go back and upload some.")
    else:
        # Removed the white banner: the <div class='result-box'> wrapper is no longer used.
        if st.session_state.selected_operation == "caption":
            # Here, processed_files is assumed to be a list of (image_path, caption) tuples.
            for image_path, caption in st.session_state.processed_files:
                st.image(image_path, width=300)
                st.markdown(f"**Caption:** {caption}")
        else:
            for file_path in st.session_state.processed_files:
                st.image(file_path, width=300)
    st.markdown("---")
    st.button("🔁 Start Over", on_click=lambda: st.session_state.update({
        "page": "home", "uploaded_files": [], "selected_operation": None, "processed_files": []
    }))
