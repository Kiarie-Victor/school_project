def generate_email_from_regno(regno: str) -> str:
    cleaned = regno.replace('-', '').replace('/', '')
    cleaned = cleaned.lower()
    email = f"{cleaned}@mmu.ac.ke"
    return email
