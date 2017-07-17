# finding elements on the given page with various tags

# Text box finding method

def TextBoxFinding(driver):
	elements = driver.find_elements_by_tag_name('input'); #Text box identification
	return  elements;	

# drop down Finder
