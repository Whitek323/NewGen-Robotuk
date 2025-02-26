import torch
print(torch.cuda.is_available())  # ควรเป็น True
print(torch.backends.cudnn.is_available())  # ควรเป็น True
