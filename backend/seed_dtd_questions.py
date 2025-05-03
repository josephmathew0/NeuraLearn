from models import db, DTDQuestion
from app import app

with app.app_context():
    db.session.query(DTDQuestion).delete()   # 👈 ONLY delete DTDQuestion data
    db.session.commit()

    db.create_all()  # Keeps other tables intact

    q1 = DTDQuestion(
        prompt="Fix the schema so that Title comes before Author, Year is an integer, and ISBN is optional.",
        initial_lines=[
            '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">',
            '  <xsd:element name="Library">',
            '    <xsd:complexType>',
            '      <xsd:sequence>',
            '        <xsd:element name="Book" type="BookType" maxOccurs="unbounded" />',
            '      </xsd:sequence>',
            '    </xsd:complexType>',
            '  </xsd:element>',
            '  <xsd:complexType name="BookType">',
            '    <xsd:sequence>',
            '      <xsd:element name="Author" type="xsd:string" maxOccurs="unbounded" />',
            '      <xsd:element name="Title" type="xsd:string" />',
            '    </xsd:sequence>',
            '    <xsd:attribute name="bookID" type="xsd:string" use="required" />',
            '    <xsd:attribute name="Year" type="xsd:string" use="required" />',
            '    <xsd:attribute name="ISBN" type="xsd:string" use="required" />',
            '  </xsd:complexType>',
            '</xsd:schema>'
        ],
        correct_lines=[
            '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">',
            '  <xsd:element name="Library">',
            '    <xsd:complexType>',
            '      <xsd:sequence>',
            '        <xsd:element name="Book" type="BookType" maxOccurs="unbounded" />',
            '      </xsd:sequence>',
            '    </xsd:complexType>',
            '  </xsd:element>',
            '  <xsd:complexType name="BookType">',
            '    <xsd:sequence>',
            '      <xsd:element name="Title" type="xsd:string" />',
            '      <xsd:element name="Author" type="xsd:string" maxOccurs="unbounded" />',
            '    </xsd:sequence>',
            '    <xsd:attribute name="bookID" type="xsd:string" use="required" />',
            '    <xsd:attribute name="Year" type="xsd:integer" use="required" />',
            '    <xsd:attribute name="ISBN" type="xsd:string" use="optional" />',
            '  </xsd:complexType>',
            '</xsd:schema>'
        ]
    )

    q2 = DTDQuestion(
        prompt="Fix the schema so Product has Name then Price, and currency is optional.",
        initial_lines=[
            '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">',
            '  <xsd:element name="Store">',
            '    <xsd:complexType>',
            '      <xsd:sequence>',
            '        <xsd:element name="Product" type="ProductType" maxOccurs="1" />',
            '      </xsd:sequence>',
            '    </xsd:complexType>',
            '  </xsd:element>',
            '  <xsd:complexType name="ProductType">',
            '    <xsd:sequence>',
            '      <xsd:element name="Price" type="xsd:decimal" />',
            '      <xsd:element name="Name" type="xsd:string" />',
            '    </xsd:sequence>',
            '    <xsd:attribute name="currency" type="xsd:string" use="required" />',
            '  </xsd:complexType>',
            '</xsd:schema>'
        ],
        correct_lines=[
            '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">',
            '  <xsd:element name="Store">',
            '    <xsd:complexType>',
            '      <xsd:sequence>',
            '        <xsd:element name="Product" type="ProductType" maxOccurs="unbounded" />',
            '      </xsd:sequence>',
            '    </xsd:complexType>',
            '  </xsd:element>',
            '  <xsd:complexType name="ProductType">',
            '    <xsd:sequence>',
            '      <xsd:element name="Name" type="xsd:string" />',
            '      <xsd:element name="Price" type="xsd:decimal" />',
            '    </xsd:sequence>',
            '    <xsd:attribute name="currency" type="xsd:string" use="optional" />',
            '  </xsd:complexType>',
            '</xsd:schema>'
        ]
    )

    db.session.add_all([q1, q2])
    db.session.commit()
    print("✅ DTD questions inserted successfully!")
