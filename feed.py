import yaml
import xml.etree.ElementTree as xml_tree

# https://help.apple.com/itc/podcasts_connect/#/itcbaf351599

with open('feed.yaml', 'r') as file:
    # use this function to load the file
    yaml_data = yaml.safe_load(file)

# create rss tag using the rss feed sample
rss_element = xml_tree.Element('rss', {
    'version': '2.0',
    'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
})

rss_channel = xml_tree.SubElement(rss_element, 'channel')

link_prefix = yaml_data['link']

# access from feed.yaml file in our directory
xml_tree.SubElement(rss_channel, 'title').text = yaml_data['title']
xml_tree.SubElement(rss_channel, 'format').text = yaml_data['format']
xml_tree.SubElement(rss_channel, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(rss_channel, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(rss_channel, 'description').text = yaml_data['description']
xml_tree.SubElement(rss_channel, 'itunes:image', {'href': link_prefix + yaml_data['image']})
xml_tree.SubElement(rss_channel, 'language').text = yaml_data['language']
xml_tree.SubElement(rss_channel, 'link').text = link_prefix
xml_tree.SubElement(rss_channel, 'itunes:category', {'text': yaml_data['category']})

for item in yaml_data['item']:
    xml_item = xml_tree.SubElement(rss_channel, 'item')
    xml_tree.SubElement(xml_item, 'title').text = item['title']
    xml_tree.SubElement(xml_item, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(xml_item, 'description').text = item['description']
    xml_tree.SubElement(xml_item, 'itunes:duration').text = item['duration']
    xml_tree.SubElement(xml_item, 'pubDate').text = item['published']

    enclosure = xml_tree.SubElement(xml_item, 'enclosure', {
        'url': link_prefix + item['file'],
        'type': 'audio/mpeg',
        'length': item['length']
    })

output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)