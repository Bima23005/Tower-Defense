# Tower-Defense
🗺️ Inisialisasi Grid dan Tower

Grid

Matriks 2D sebagai peta.

S: Start (musuh mulai)

G: Goal (tujuan musuh)

T: Tower

.: Jalur kosong

Tower

Dictionary berisi posisi tower sebagai key dan data (range, damage, cooldown).

cd_now melacak waktu cooldown saat ini.


🧠 Fungsi Heuristik

Jarak Manhattan antara dua titik.

Dipakai oleh GBFS untuk menilai seberapa dekat suatu titik ke tujuan.


🧭 Greedy Best-First Search

Penjelasan inti:

Inisialisasi queue dengan (heuristik(start), start)

Selama queue tidak kosong:

Ambil node dengan prioritas terendah (paling dekat ke goal).

Tandai sebagai dikunjungi.

Tambahkan tetangga valid ke queue.

Simpan jejak (came_from) untuk merekonstruksi jalur nanti.

