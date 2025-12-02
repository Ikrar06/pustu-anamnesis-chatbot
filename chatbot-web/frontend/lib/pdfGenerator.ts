import jsPDF from 'jspdf';

interface PDFData {
  patientName: string;
  timestamp: string;
  summaryText: string;
}

export function generateAnamnesisPDF(data: PDFData) {
  const doc = new jsPDF();

  // Set font (jsPDF includes Helvetica by default)
  doc.setFont('helvetica');

  // Header
  doc.setFontSize(18);
  doc.setFont('helvetica', 'bold');
  doc.text('HASIL ANAMNESIS PASIEN', 105, 20, { align: 'center' });

  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text('Chatbot PUSTU - Puskesmas Pembantu', 105, 28, { align: 'center' });

  // Separator line
  doc.setLineWidth(0.5);
  doc.line(15, 33, 195, 33);

  // Metadata
  doc.setFontSize(9);
  doc.setFont('helvetica', 'italic');
  doc.text(`Tanggal: ${data.timestamp}`, 15, 40);

  // Main content
  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');

  // Parse and format the summary text
  const lines = data.summaryText.split('\n');
  let currentY = 50;
  const lineHeight = 6;
  const pageHeight = doc.internal.pageSize.height;
  const marginBottom = 20;

  for (const line of lines) {
    // Check if we need a new page
    if (currentY > pageHeight - marginBottom) {
      doc.addPage();
      currentY = 20;
    }

    // Handle different line types
    if (line.startsWith('===')) {
      // Double line separator
      doc.setLineWidth(0.3);
      doc.line(15, currentY, 195, currentY);
      currentY += 4;
    } else if (line.startsWith('---')) {
      // Single line separator
      doc.setLineWidth(0.1);
      doc.line(15, currentY, 195, currentY);
      currentY += 4;
    } else if (line.includes('IDENTITAS PASIEN') || line.includes('ANAMNESIS') || line.includes('RIWAYAT MEDIS')) {
      // Section headers
      doc.setFontSize(12);
      doc.setFont('helvetica', 'bold');
      doc.text(line, 15, currentY);
      currentY += lineHeight + 2;
      doc.setFontSize(10);
      doc.setFont('helvetica', 'normal');
    } else if (line.includes(':')) {
      // Field: Value pairs
      const [field, ...valueParts] = line.split(':');
      const value = valueParts.join(':').trim();

      doc.setFont('helvetica', 'bold');
      doc.text(field.trim() + ':', 15, currentY);

      doc.setFont('helvetica', 'normal');
      // Handle long values with text wrapping
      const maxWidth = 120;
      const valueLines = doc.splitTextToSize(value, maxWidth);
      doc.text(valueLines, 70, currentY);
      currentY += lineHeight * valueLines.length;
    } else if (line.trim() === '') {
      // Empty line
      currentY += 3;
    } else {
      // Regular text with wrapping
      const maxWidth = 180;
      const textLines = doc.splitTextToSize(line, maxWidth);
      doc.text(textLines, 15, currentY);
      currentY += lineHeight * textLines.length;
    }
  }

  // Footer
  const totalPages = doc.internal.pages.length - 1;
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setFont('helvetica', 'italic');
    doc.text(
      `Halaman ${i} dari ${totalPages}`,
      105,
      pageHeight - 10,
      { align: 'center' }
    );
    doc.text(
      'Dokumen ini dihasilkan secara otomatis oleh Chatbot PUSTU',
      105,
      pageHeight - 6,
      { align: 'center' }
    );
  }

  // Generate filename with timestamp
  const filename = `Anamnesis_${data.patientName.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;

  // Save the PDF
  doc.save(filename);
}

// Helper function to extract patient name from summary text
export function extractPatientName(summaryText: string): string {
  const nameMatch = summaryText.match(/Nama\s+:\s+(.+)/);
  return nameMatch ? nameMatch[1].trim() : 'Pasien';
}

// Helper function to format current timestamp
export function formatTimestamp(): string {
  const now = new Date();
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'Asia/Jakarta'
  };
  return now.toLocaleDateString('id-ID', options) + ' WIB';
}
