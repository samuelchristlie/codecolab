import os
import subprocess

from pycloudflared import try_cloudflare


try:
	from google.colab import drive

	on_colab = True

except ImportError:
	on_colab = False


EXTENSIONS = ["ms-toolsai.jupyter", "ms-toolsai.vscode-jupyter-cell-tags",
			  "ms-toolsai.jupyter-keymap", "ms-toolsai.jupyter-renderers",
			  "ms-python.python", "esbenp.prettier-vscode",
			  "vscode-icons-team.vscode-icons"
			  ]

class CodeColab:
	def __init__(
		self,
		port = 8050,
		password = None,
		mount_drive = False,
	):
		self.port = port
		self.password = password
		self.mount_drive = mount_drive

		self.install_codeserver()
		self.install_extensions()
		self.start_cloudflared()		
		self.start_codeserver()

	@staticmethod
	def install_codeserver():
		subprocess.run(["curl", "-O",
						"https://raw.githubusercontent.com/coder/code-server/main/install.sh"
					   ],
					   # stdout = subprocess.PIPE
					   )

		subprocess.run(["sh", "install.sh"
					   ],
					   # stdout = subprocess.PIPE
					   )

	@staticmethod
	def install_extensions():
		for extension in EXTENSIONS:
			subprocess.run(["code-server", "--install-extension", extension
			],
			# stdout = subprocess.PIPE
			)

	def start_codeserver(self):
		os.system(f"fuser -n tcp -k {self.port}")

		if self.mount_drive and on_colab:
			drive.mount("/content/drive")

		if self.password:
			command = f"PASSWORD={self.password} code-server --port {self.port} --disable-telemetry"
		else:
			command = f"code-server --port {self.port} --auth none --disable-telemetry"

		with subprocess.Popen([command],
							 shell = True,
							 bufsize = 1,
							 universal_newlines = True,
							 stdout = subprocess.PIPE
							 ) as process:
			for line in process.stdout:
				print(line, end = "")

	def start_cloudflared(self):
		url = try_cloudflare(port = self.port).tunnel

		print(f"VSCode can be accessed on {url}")

