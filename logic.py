from reportlab.pdfgen import canvas as pdf_container
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

'''Contains methods to split lengthy sections so that they are able to fit within the pdf. After splitting the
sections, it appends the newly formed sections to the "to_pdf_holder". '''


class ModelGeneratePDF:
    def __init__(self, manager, path, file_name):
        self.font = "Courier"
        self.font_size = 14
        self.name = file_name
        self.file_path = path + "/" + self.name + ".pdf"
        self.manager = manager
        self.to_pdf_holder = []
        self.start_height = 50
        self.vertical_offset = 10 + ((self.font_size - 12) * 1.5)
        self.new_pdf = pdf_container.Canvas(self.file_path, pagesize=letter, bottomup=0)
        self.new_pdf.setFont(self.font, size=self.font_size)
        self.start_index = 0
        self.end_index = 0

# Splits long sections into multiple sections to prevent overflow
    def split_sections(self, access_to_section, start_index, end_index, name, add_string_control):
        length_limit = 58
        if len(access_to_section.section[0][start_index:]) > length_limit:
            new_song_section = SongSection(name=name)
            if add_string_control == 0:
                new_song_section.section.append(access_to_section.section[0][start_index:end_index])
                new_song_section.section.append(access_to_section.section[1][start_index:end_index])
                new_song_section.section.append(access_to_section.section[2][start_index:end_index])
                new_song_section.section.append(access_to_section.section[3][start_index:end_index])
                new_song_section.section.append(access_to_section.section[4][start_index:end_index])
                new_song_section.section.append(access_to_section.section[5][start_index:end_index])
                start_index += 62
                end_index += 58
            else:
                new_song_section.section.append("e|" + access_to_section.section[0][start_index:end_index])
                new_song_section.section.append("B|" + access_to_section.section[1][start_index:end_index])
                new_song_section.section.append("G|" + access_to_section.section[2][start_index:end_index])
                new_song_section.section.append("D|" + access_to_section.section[3][start_index:end_index])
                new_song_section.section.append("A|" + access_to_section.section[4][start_index:end_index])
                new_song_section.section.append("E|" + access_to_section.section[5][start_index:end_index])
                start_index += 58
                end_index += 58
            self.to_pdf_holder.append(new_song_section)
            self.split_sections(access_to_section, start_index, end_index, name, 1)
        else:
            new_song_section = SongSection(name=name)
            if add_string_control == 0:
                new_song_section.section.append(access_to_section.section[0][start_index:end_index])
                new_song_section.section.append(access_to_section.section[1][start_index:end_index])
                new_song_section.section.append(access_to_section.section[2][start_index:end_index])
                new_song_section.section.append(access_to_section.section[3][start_index:end_index])
                new_song_section.section.append(access_to_section.section[4][start_index:end_index])
                new_song_section.section.append(access_to_section.section[5][start_index:end_index])
            else:
                new_song_section.section.append("e|" + access_to_section.section[0][start_index:end_index])
                new_song_section.section.append("B|" + access_to_section.section[1][start_index:end_index])
                new_song_section.section.append("G|" + access_to_section.section[2][start_index:end_index])
                new_song_section.section.append("D|" + access_to_section.section[3][start_index:end_index])
                new_song_section.section.append("A|" + access_to_section.section[4][start_index:end_index])
                new_song_section.section.append("E|" + access_to_section.section[5][start_index:end_index])
            self.to_pdf_holder.append(new_song_section)

# This function is used to gather sections, decide if they need to be split, and pass them to "split_sections" method if
# necessary.

    def gather_sections(self):
        temp_start_index = 0
        temp_end_index = 62
        for section_name in self.manager.second_screen_content.listview_array:
            for section in self.manager.first_screen_content.section_holder:
                if section_name == section.name:
                    if len(section.section[0]) > temp_end_index:
                        self.split_sections(section, temp_start_index, temp_end_index, section.name, 0)
                    else:
                        self.to_pdf_holder.append(section)
                    temp_start_index = 0
                    temp_end_index = 62

    #

    def draw_sections_to_pdf(self):
        holder = 0
        holder_vertical_offset = self.vertical_offset
        for section in self.to_pdf_holder:
            self.new_pdf.drawString(1*inch, self.start_height + (holder * holder_vertical_offset), section.section[0])
            holder += 1
            self.new_pdf.drawString(1*inch, self.start_height + (holder * holder_vertical_offset), section.section[1])
            holder += 1
            self.new_pdf.drawString(1*inch, self.start_height + (holder * holder_vertical_offset), section.section[2])
            holder += 1
            self.new_pdf.drawString(1*inch, self.start_height + (holder * holder_vertical_offset), section.section[3])
            holder += 1
            self.new_pdf.drawString(1*inch, self.start_height + (holder * holder_vertical_offset), section.section[4])
            holder += 1
            self.new_pdf.drawString(1*inch, self.start_height + (holder * holder_vertical_offset), section.section[5])
            holder += 1
            self.start_height += 20
        self.new_pdf.save()


class SongSection:
    def __init__(self, name):
        self.section = []
        self.name = name
