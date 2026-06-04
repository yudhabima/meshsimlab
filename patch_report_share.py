# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path('simulasimain.html')
text = path.read_text(encoding='utf-8')

new_download = r'''function downloadReport(){
    const acc=attempts>0?Math.round((corrects/attempts)*100):0;
    let text=`LAPORAN SIMULASI TRANSMISI\n===============================\nNama: ${userName}\nAbsen: ${userAbsen}\nTanggal: ${new Date().toLocaleDateString('id-ID')}\n===============================\nPercobaan: ${attempts} | Benar: ${corrects} | Akurasi: ${acc}%\n\nRiwayat:\n`;
    log.slice(-5).forEach((e,i)=>{text+=`${i+1}. ${e.gear} [${e.status}] ${e.time}\n`;});
    const jsPDF = window.jspdf?.jsPDF;
    if(!jsPDF){
        showToast('⚠ Gagal membuat PDF. Muat ulang halaman dan coba lagi.', 'error');
        return;
    }
    const doc = new jsPDF({ unit: 'pt', format: 'a4' });
    doc.setFont('Helvetica', 'normal');
    doc.setFontSize(10);
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 40;
    const content = doc.splitTextToSize(text, pageWidth - margin * 2);
    doc.text(content, margin, 50);
    const safeName = userName ? userName.replace(/\s+/g, '_') : 'laporan';
    doc.save(`Laporan_Simulasi_${safeName}.pdf`);
}
'''

new_whatsapp = r'''function openShareModal(){
    const acc=attempts>0?Math.round((corrects/attempts)*100):0;
    let text=`⚙ SIMULASI TRANSMISI\nNama: ${userName} | Absen: ${userAbsen}\nPercobaan: ${attempts} | Benar: ${corrects} | Akurasi: ${acc}%\n`;
    log.slice(-5).forEach((e,i)=>{text+=`${i+1}. ${e.gear} [${e.status}] ${e.time}\n`;});
    const url = 'https://wa.me/?text=' + encodeURIComponent(text);
    window.open(url, '_blank');
}
'''

text = re.sub(r'function downloadReport\(\)\{.*?\n\}', lambda m: new_download, text, flags=re.S)
text = re.sub(r'function openShareModal\(\)\{.*?\n\}', lambda m: new_whatsapp, text, flags=re.S)
path.write_text(text, encoding='utf-8')
print('patched')
