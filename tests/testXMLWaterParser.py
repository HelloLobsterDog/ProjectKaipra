import unittest
from dirt.XMLWaterParser import XMLWaterParser

class XMLNodeTests(unittest.TestCase):

	def test_XMLWaterParser_formatTextBlock(self):
		''' basically the same test as the Node.formatTextBlock happy path test, but gets the node from xml '''
		parser = XMLWaterParser(fromString = '''<?xml version="1.0"?>
<water default_lang="en-us">
	<node id="one">
		<text_block lang="en-us">
			hell{favorite_vowel} {win_or_loss}{conjunction}{weight_abbreviation}!
		</text_block>
		<check name="favorite_vowel" type="choice" based_on="node.vowel">
			<option> <if> 0 </if> <then> a </then> </option>
			<option> <if> 1 </if> <then> e </then> </option>
			<option> <if> 2 </if> <then> i </then> </option>
			<option> <if> 3 </if> <then> o </then> </option>
			<option> <if> 4 </if> <then> u </then> </option>
			<option> <anything_else/> <then> y </then> </option>
		</check>
		<check name="win_or_loss" type="bool" based_on="node.victory">
			<true> <then> w </then> </true>
			<false> <then> l </then> </false>
		</check>
		<check name="conjunction" type="choice" based_on="node.day_in_month">
			<option> <if> 0 </if> <if> 1 </if> <then> for </then> </option>
			<option> <if> 2 </if> <if> 3 </if> <then> and </then> </option>
			<option> <if> 4 </if> <if> 5 </if> <then> nor </then> </option>
			<option> <if> 6 </if> <if> 7 </if> <then> but </then> </option>
			<option> <if> 8 </if> <if> 9 </if> <then> or </then> </option>
			<option> <if> 10 </if> <if> 11 </if> <then> yet </then> </option>
			<option> <if> 12 </if> <if> 13 </if> <anything_else/> <then> so </then> </option>
		</check>
		<check name="weight_abbreviation" type="comparison" based_on="node.weight">
			<option> <less_than> 4.2 </less_than> <then formatted="true"> l{d} </then> </option>
			<option> <equal> 4.2 </equal> <then> g </then> </option>
			<option> <greater_than> 4.2 </greater_than> <then> kg </then> </option>
		</check>
		<check name="d" type="bool" based_on="node.b">
			<true> <then> b </then> </true>
			<false> <then> d </then> </false>
		</check>
		
		<state_var name="vowel" type="integer" default="3" />
		<state_var name="victory" type="boolean" default="True" />
		<state_var name="day_in_month" type="integer" default="8" />
		<state_var name="weight" type="decimal" default="1.4" />
		<state_var name="b" type="boolean" default="False" />
	</node>
</water>''')
		
		water = parser.parse()
		theNode = water.getNode('one')
		self.assertIsNotNone(theNode)
		self.assertEqual('hello world!', theNode.formatTextBlock('en-us'))
		