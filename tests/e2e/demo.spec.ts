import {test,expect} from '@playwright/test';
test('complete factory story, original sources, and inspection handover',async({page})=>{
 await page.goto('/');
 await page.getByRole('button',{name:'Review the evidence',exact:true}).click();
 await expect(page.getByRole('dialog',{name:'Mira’s evidence workbench'})).toBeVisible();
 await expect(page.getByRole('button',{name:'Next: supplier report'})).toBeDisabled();
 await page.getByRole('button',{name:'Scan this evidence',exact:true}).click();
 await page.getByRole('button',{name:'Next: supplier report'}).click();
 await page.getByRole('button',{name:'Scan this evidence',exact:true}).click();
 await page.getByRole('button',{name:'Next: factory ledgers'}).click();
 for(const id of ['E4','E5']){
  await page.getByRole('button',{name:new RegExp('FACTORY LEDGER.*'+id)}).click();
  await expect(page.getByRole('table')).toBeVisible();
  await page.getByRole('button',{name:'Return to baseline review'}).click();
  await expect(page.getByRole('button',{name:'Confirm baseline & follow the line'})).toBeVisible();
 }
 await page.getByRole('button',{name:'Confirm baseline & follow the line'}).click();
 await expect(page.getByRole('heading',{name:'Follow the bottle.'})).toBeVisible();
 await page.getByRole('button',{name:'Recover the missing record',exact:true}).click();
 await page.getByRole('button',{name:'Inspect recovered evidence'}).click();
 await page.getByRole('button',{name:'Extract from source'}).click();
 await page.getByRole('button',{name:'Confirm relationship'}).click();
 await page.getByRole('button',{name:'Walk to dispatch office'}).click();
 await expect(page.locator('.ticket-number')).toContainText('1,500');
 await page.getByRole('button',{name:'Write the inspection proposal'}).click();
 await page.getByLabel('Reviewer note').fill('Inspect connected shipments. Original records and recovered slip reviewed.');
 await page.getByRole('button',{name:'Save reviewed snapshot'}).click();
 await expect(page.getByRole('heading',{name:'A handover you can stand behind.'})).toBeVisible();
 const [download]=await Promise.all([page.waitForEvent('download'),page.getByRole('link',{name:'Download report'}).click()]);
 expect(download.suggestedFilename()).toBe('batchlens-inspection.html');
 await page.reload();await page.getByRole('button',{name:'Crew rooms',exact:true}).click();
 await page.getByRole('button',{name:'03 Dispatch office'}).click();
 await expect(page.getByRole('link',{name:'Download report'})).toBeVisible();
});
test('mobile evidence wall, search and pause persist across rooms',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/');
 await page.getByRole('button',{name:'Pause motion',exact:true}).click();
 await page.getByRole('button',{name:'Crew rooms',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Every clue has a story.'})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBeTruthy();
 await expect(page.getByRole('button',{name:'Resume motion'})).toBeVisible();
 await page.getByRole('button',{name:'Find evidence'}).click();
 await page.getByRole('textbox',{name:'Search evidence'}).fill('supplier');
 await page.getByRole('button',{name:/Supplier inspection/}).click();
 await expect(page.getByRole('dialog',{name:'Supplier inspection'})).toBeVisible();
 await page.keyboard.press('Escape');await expect(page.getByRole('dialog')).toHaveCount(0);
 await page.getByRole('button',{name:'Take a seat at the workbench'}).click();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBeTruthy();
});
