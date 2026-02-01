from engine.engine import EncryptionEngine

def test_encrypt_decrypt_cycle():
    engine = EncryptionEngine()
    text = "Hello World! 123"
    encrypted = engine.encrypt(text)
    decrypted = engine.decrypt(encrypted)
    assert decrypted == text

